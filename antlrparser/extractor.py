import os
import re
import logging
from config.config import DEFAULT_SCHEMA, DELIMITER
from sqlparse import format as fmt
from sql.objects import Query, Procedure, Table
from antlr4 import *
from antlrparser.lexer import MySqlLexer
from antlrparser.parser import MySqlParser
from typing import Tuple, List, Optional

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Mapper:

    """Helper class used to map DML extraction regexes with parsing methods.
    Also provides cleanup regexes used to deal with edge cases, e.g. table names
    containing SQL keywords"""

    def __init__(self):

        self.extract_regexes = \
            {'INSERT': re.compile("INSERT\s+?INTO.*?;", re.DOTALL | re.IGNORECASE),
             'REPLACE': re.compile("REPLACE\s+?INTO.*?;", re.DOTALL | re.IGNORECASE),
             'UPDATE': re.compile("UPDATE\s+.*?;", re.DOTALL | re.IGNORECASE),
             'DELETE': re.compile("DELETE\s+?FROM.*?;", re.DOTALL | re.IGNORECASE)}

        self.cleanup_regexes = {re.compile("ON\s+DUPLICATE\s+KEY\s+UPDATE.*?;", re.DOTALL | re.IGNORECASE): ";",
                                re.compile("INSTALL"): "INST"}

        self.methods = None
        self.parser = None
        self.extractors = None
        self.parsermethods = None
        self.mapper = None

    def map_methods(self, walker):

        """
        Maps the required regexes and functions by DML type.

        :param walker: Treewalker object
        """

        methods = \
            {'INSERT': self.parser.insertStatement,
             'REPLACE': self.parser.replaceStatement,
             'UPDATE': self.parser.updateStatement,
             'DELETE': self.parser.deleteStatement}

        self.extractors = \
            {'INSERT': walker.parse_insert,
             'REPLACE': walker.parse_insert,
             'UPDATE': walker.parse_update,
             'DELETE': walker.parse_delete}

        self.parsermethods = methods
        self.mapper = {k: {'regex': v} for k, v in self.extract_regexes.items()}
        for k in self.mapper.keys():
            self.mapper[k]['parsermethod'] = self.parsermethods[k]
            self.mapper[k]['extractor'] = self.extractors[k]


class FileProcessor:

    """Main class managing all the parsing operations
    processing using ANTLR-generated objects"""

    # TODO -> Move settings to Config object
    # TODO -> Ensure regexes are compiled only once

    def __init__(self):

        self.results = []
        self.errored = []
        self.default_schema = DEFAULT_SCHEMA

    def parse_dir(self, dir_path: str) -> None:

        """
        Walks through a given directory, parses SQL procedures in all SQL files found,
        appends Procedure objects created to self.results.

        :param dir_path: path to the target directory
        :param delimiter: delimiter enabling antlrparser of CREATE PROCEDURE statements, defaults to ";;"
        :param topdown: optional parameter controlling the directory "walking" behavior, defaults to False
        """

        # Walk through directory
        for root, dirs, files in os.walk(dir_path, topdown=False):
            # Loop on .sql files
            for name in files:
                if name.endswith('.sql'):
                    path = f'{root}/{name}'
                    self.parse_file(path)

    def parse_file(self, path: str) -> None:

        """
        Finds and parses all procedures in SQL file.

        :param path: file path
        """

        PROCEDURE_REGEX = re.compile(f"CREATE\s+?PROCEDURE.*?{DELIMITER}", re.DOTALL | re.IGNORECASE)

        with open(path, 'r') as file:
            # Grammar is case-sensitive. Input has to be converted
            # to upper case before parsing
            input = fmt(file.read().upper(), strip_comments=True).strip()

            # Find all CREATE PROCEDURE statements and parse them
            procedures = re.findall(PROCEDURE_REGEX, input)
            for proc in procedures:
                self.parse_procedure(path, proc)

    def parse_object_name(self, name: str) -> Tuple[str, str]:

        """
        Separates name and schema from a raw database object name.
        If no schema is foiund, uses the default schema defined
        in the configuration.

        :param name: raw table name
        :return: tuple (schema_string, name_string)
        """

        # TODO -> Move to utils.utils by adding default_schema parameter

        if '.' in name:
            schema = name.split('.')[0]
            name = name.split('.')[1]
        else:
            schema = self.default_schema

        return schema, name

    def get_procedure_name(self, p: str) -> Tuple[str, str]:

        """
        Gets the procedure name from the procedure body.

        :param p: procedure string
        :return: tuple (schema_string, name_string)
        """

        NAME_REGEX = re.compile(f"(?<=CREATE\sPROCEDURE\s)(?:IF\s+(NOT\s+)?EXISTS\s+)?([a-zA-Z.]+)", re.IGNORECASE)
        name = re.search(NAME_REGEX, p).group().lower()
        schema, name = self.parse_object_name(name)
        return schema, name

    def parse_procedure(self, path: str, p: str) -> None:

        """
        Gets all configured DML statements inside a procedure body, parses them,
        stores results in Procedure objects, and appends these objects to
        self.results.

        :param path: the procedure path is passed here as the Procedure instantiation
        requires it.
        :param p: procedure body as string
        """

        schema, name = self.get_procedure_name(p)
        proc = Procedure(path, name=name, schema=schema)

        mapper = Mapper()

        for dmltype in mapper.extract_regexes.keys():
            statements = re.findall(mapper.extract_regexes[dmltype], p)
            for s in statements:
                q = self.parse_statement(dmltype, s, mapper)
                if q:
                    q.procedure = name
                    proc.queries.append(q)

        self.results.append(proc)

    def parse_statement(self, dmltype: str, s: str, mapper: Mapper) -> Query:

        """
        Cleans DML statement, creates parsing objects, and returns a Query object.

        :param dmltype: type of DML statement being parsed
        :param s: DML statement string
        :param mapper: Mapper object
        :return: Query object containing the statement information
        """

        s = self.cleanup_statement(s, mapper)
        input = InputStream(s)
        lexer = MySqlLexer(input)
        stream = CommonTokenStream(lexer)
        parser = MySqlParser(stream)
        mapper.parser = parser
        mapper.map_methods(self)
        tree = mapper.mapper[dmltype]['parsermethod']()
        r = mapper.mapper[dmltype]['extractor'](tree, dmltype)
        return r

    def get_updated_columns(self, tree: ParserRuleContext) -> List[str]:

        """
        Loops recursively over AST children and gathers all the updated columns.

        :param tree: AST object parsed
        :return: list containing all update details
        """

        cols = []
        for c in tree.getChildren():

            if isinstance(c, MySqlParser.UpdatedElementContext):
                cols.append(c.getText().lower())
            elif not isinstance(c, TerminalNode):
                cols.extend(self.get_updated_columns(c))

        return cols

    def get_inserted_columns(self, tree: ParserRuleContext) -> List[str]:

        """
        Loops recursively over AST children and gathers all the inserted columns.

        :param tree: AST object parsed
        :return: list of columns being inserted into
        """

        for child in tree.getChildren():
            if isinstance(child, MySqlParser.UidListContext):
                target_columns = child.getText().lower().split(",")
                return target_columns

        target_columns = []
        return target_columns

    def parse_update(self, tree: ParserRuleContext, dmltype: str) -> Optional[Query]:

        """
        Parses target table, source table(s) and target columns from
        an UPDATE statement.

        :param tree: AST object parsed
        :param dmltype: DML statement type is passed for Query object instantiation
        :return: Query object containing the statement information
        """

        q = Query(operation=dmltype)

        q.target_table = self.get_first_table(tree)
        q.from_table = self.get_source_tables(tree)
        q.target_columns = self.get_updated_columns(tree)

        if q.target_table and q.from_table:
            return q

    def get_inserted_tables(self, tree: ParserRuleContext) -> Optional[List[Table]]:

        """
        Gets all source tables from an INSERT statement.

        :param tree: AST object parsed
        :return: list of source tables names string
        """

        for child in tree.getChildren():
            if isinstance(child, MySqlParser.InsertStatementValueContext):
                return self.get_source_tables(child)

    def parse_insert(self, tree: ParserRuleContext, dmltype: str) -> Query:

        """
        Parses target table, source table(s) and target columns from
        an INSERT statement.

        :param tree: AST object parsed
        :param dmltype: DML statement type for Query object instantiation
        :return: Query object containing the statement information
        """

        q = Query(operation=dmltype)
        q.target_table = self.get_first_table(tree)
        q.from_table = self.get_inserted_tables(tree)
        q.target_columns = self.get_inserted_columns(tree)

        return q

    def get_delete_table(self, tree: ParserRuleContext) -> Optional[List[Table]]:

        """
        Gets the table name from a DELETE statement.

        :param tree: AST object parsed
        :return: the target table name
        """

        for child in tree.getChildren():
            if isinstance(child, MySqlParser.DeleteStatementValueContext):
                return self.get_source_tables(child)

    def parse_delete(self, tree: ParserRuleContext, dmltype: str) -> Query:

        """
        Parses the target table from a DELETE statement
        :param tree: AST object parsed
        :param dmltype: DML statement type for Query object instantiation
        :return: Query object containing the statement information
        """

        q = Query(operation=dmltype)
        q.target_table = self.get_first_table(tree)

        return q

    def cleanup_statement(self, s: str, mapper: Mapper) -> str:

        """
        Iterates over a Mapper object's cleanup_regexes dict to replace eventual edge cases in
        a statement body, e.g. keywords contained in a table name.

        :param s: string to replace into
        :param mapper: Mapper object
        :return: new string value
        """

        # TODO -> Move to utils.utils

        for k, v in mapper.cleanup_regexes.items():
            s = re.sub(k, v, s)
        return s

    def get_source_tables(self, tree: ParserRuleContext) -> List[Table]:

        """
        Collects recursively table names in FROM and JOIN clauses in a statement.

        :param tree: AST object parsed
        :return: list of source tables
        """

        tables = []

        for c in tree.getChildren():

            if isinstance(c, MySqlParser.JoinPartContext) or isinstance(c, MySqlParser.FromClauseContext):
                tables.extend(self.get_all_tables(c))
            elif not (isinstance(c, TerminalNode) or isinstance(c, ErrorNode)):
                tables.extend(self.get_source_tables(c))

        return tables

    def get_first_table(self, tree: ParserRuleContext) -> Table:

        """
        Walks recursively to the first table name found in a statement AST and returns it.

        :param tree: AST object parsed
        :return: table name string
        """

        for c in tree.getChildren():

            if isinstance(c, MySqlParser.TableNameContext):
                schema, name = self.parse_object_name(c.getText().lower())
                t = Table(name, schema)
                return t
            elif not (isinstance(c, TerminalNode) or isinstance(c, MySqlParser.JoinPartContext)):
                return self.get_first_table(c)

    def get_all_tables(self, tree: ParserRuleContext) -> List[Table]:

        """
        Gets all table names inside a tree, appends them to a list of table names and returns it

        :param tree: AST object parsed
        :return: list of table names
        """

        tables = []
        for child in tree.getChildren():
            if isinstance(child, MySqlParser.TableNameContext):
                schema, name = self.parse_object_name(child.getText().lower())
                t = Table(name, schema)
                tables.append(t)
            elif not (isinstance(child, TerminalNode) or isinstance(child, ErrorNode)):
                tables.extend(self.get_all_tables(child))
        return tables
