import os
import re
import multiprocessing as mp
from parse.regex import procedure_regex, NAME_REGEX
from sqlparse import format as fmt
from sql.objects import Procedure
from antlr4 import ParserRuleContext, TerminalNode, ErrorNode, \
    InputStream, CommonTokenStream
from parse.lexer import MySqlLexer
from parse.parser import MySqlParser
from parse.mapper import Mapper
from sql.objects import Statement, Table
from typing import List, Tuple, Optional


class Runner:

    """Main class managing all the parsing operations
    processing using ANTLR-generated objects"""

    def __init__(self, default_schema: str, delimiter: str, mode: str) -> None:

        self.results = []
        self.delimiter = delimiter
        self.proc_regex = procedure_regex(self.delimiter)
        self.default_schema = default_schema
        self.mode = mode

    def run(self, path):

        if os.path.isdir(path):
            self.parse_dir(path)
        elif os.path.isfile(path):
            self.results = self.parse_file(path)
    
    def parse_dir(self, dir_path: str) -> None:

        """
        Walks through a given directory, parses SQL procedures in all SQL
        files found, appends Procedure objects to self.results.

        :param dir_path: path to the target directory
        """

        # Create multiprocessing pool
        pool = mp.Pool()
        sql_files = []
        # Walk through directory
        for root, dirs, files in os.walk(dir_path, topdown=False):
            # Loop on .sql files
            for name in files:
                if name.endswith('.sql'):
                    sql_files.append(f'{root}/{name}')
        results = pool.map(self.parse_file, sql_files)
        self.results = [p for file in results for p in file]

    def parse_file(self, path: str) -> List[Procedure]:

        """
        Finds and parses all procedures in SQL file.

        :param path: file path
        """

        results = []

        with open(path, 'r') as file:
            # Grammar is case-sensitive. Input has to be converted
            # to upper case before parsing
            file_input = fmt(file.read().upper().replace('`', ''), strip_comments=True).strip()

            # Parsing modes switch
            if self.mode == 'procedure':
                procedures = re.findall(self.proc_regex, file_input)
                for proc in procedures:
                    results.append(self.parse_str(path, proc))
            elif self.mode == 'ddl':
                results.append(self.parse_str(path, file_input))

        return results

    def parse_str(self, path: str, p: str) -> Procedure:

        """
        Gets all configured DML statements inside a procedure body,
        parses them, stores results in Procedure objects, and appends
        these objects to self.results.

        :param path: the procedure path is passed here as the Procedure
        instantiation requires it.
        :param p: procedure body string
        :param mode: parsing mode, "procedure" or "ddl"
        """

        if self.mode == 'procedure':
            schema, name = self.get_procedure_name(p)
        elif self.mode == 'ddl':
            schema, name = '', path
        proc = Procedure(path, name=name, schema=schema, statements=[])

        mapper = Mapper(self.delimiter, self.mode)

        for dmltype in mapper.extract_regexes.keys():
            statements = re.findall(mapper.extract_regexes[dmltype], p)
            for s in statements:
                q = self.parse_statement(dmltype, s, mapper)
                if q:
                    q.procedure = name
                    proc.statements.append(q)

        return proc

    def get_procedure_name(self, p: str) -> Tuple[str, str]:

        """
        Gets the procedure name from the procedure body.

        :param p: procedure string
        :return: tuple (schema_string, name_string)
        """

        name = re.search(NAME_REGEX, p).group(1).lower()
        schema, name = self.parse_object_name(name)
        return schema, name

    def parse_object_name(self, name: str) -> Tuple[str, str]:

        """
        Separates name and schema from a raw database object name.
        If no schema is found, uses the default schema defined
        in the configuration.

        :param name: raw table name
        :return: tuple (schema_string, name_string)
        """

        if '.' in name:
            schema = name.split('.')[0]
            name = name.split('.')[1]
        else:
            schema = self.default_schema

        return schema, name

    def parse_statement(self, dmltype: str, s: str, mapper: Mapper) -> Statement:

        """
        Cleans DML statement, creates parsing objects, and returns a
        Query object.

        :param dmltype: type of DML statement being parsed
        :param s: DML statement string
        :param mapper: Mapper object
        :return: Query object containing the statement information
        """

        input_stream = InputStream(s)
        lexer = MySqlLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = MySqlParser(token_stream)
        mapper.parser = parser
        mapper.map_methods(self)
        tree = mapper.mapper[dmltype]['parsermethod']()
        r = mapper.mapper[dmltype]['extractor'](tree, dmltype)
        return r

    def get_updated_columns(self, tree: ParserRuleContext) -> List[str]:

        """
        Loops recursively over AST children and gathers all the updated
        columns.

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
        Loops recursively over AST children and gathers all the inserted
        columns.

        :param tree: AST object parsed
        :return: list of columns being inserted into
        """

        for child in tree.getChildren():
            if isinstance(child, MySqlParser.UidListContext):
                target_columns = child.getText().lower().split(',')
                return target_columns

        target_columns = []
        return target_columns

    def parse_create_table(self, tree: ParserRuleContext, dmltype: str) \
            -> Optional[Statement]:

        """
        Parse the three types of CREATE TABLE statements existing in MySQL 5.6,
        returns as much information as possible in each case.

        :param tree: AST object parsed
        :param dmltype: DML statement type for Query object instantiation
        :return: Query object containing the statement information
        """

        q = Statement()
        q.target_table = self.get_target_table(tree)

        # Parse create table column statements
        if isinstance(tree, MySqlParser.ColumnCreateTableContext):
            q.operation = f'{dmltype} COLUMNS'
            q.target_columns = self.get_create_table_columns(tree)

        # Parse create table query statements
        elif isinstance(tree, MySqlParser.QueryCreateTableContext):
            q.operation = f'{dmltype} QUERY'
            q.from_table = self.get_source_tables_insert(tree, 'from')
            q.join_table = self.get_source_tables_insert(tree, 'join')
            try:
                query = tree.selectStatement().querySpecification()
            except AttributeError as e:
                query = tree.selectStatement().queryExpression().querySpecification()
            q.target_columns = query.selectElements().getText().lower().split(',')

        # Parse create table like statements
        elif isinstance(tree, MySqlParser.CopyCreateTableContext):
            q.operation = f'{dmltype} LIKE'
            target = self.parse_object_name(tree.tableName(0).getText().lower())
            q.target_table = Table(name=target[1], schema=target[0])
            source = self.parse_object_name(tree.tableName(1).getText().lower())
            q.from_table = [Table(name=source[1], schema=source[0])]

        return q

    def get_create_table_columns(self, tree: ParserRuleContext) -> List[str]:

        """
        Get columns definition in CREATE TABLE "columns" statement.
        :param tree: AST object parsed
        :return: list of columns found
        """

        columns = []

        for c in tree.getChildren():

            if isinstance(c, MySqlParser.ColumnDeclarationContext):
                columns.append(c.uid().getText().lower())
            elif not (isinstance(c, TerminalNode) or isinstance(c, ErrorNode)):
                columns.extend(self.get_create_table_columns(c))

        return columns

    def parse_truncate(self, tree: ParserRuleContext, dmltype: str) -> Statement:

        """
        Parse target table from TRUNCATE statement.

        :param tree: AST object parsed
        :param dmltype: DML statement type is passed for Query object
        instantiation
        :return: Query object containing the statement information
        """

        q = Statement(operation=dmltype)
        q.target_table = self.get_target_table(tree)
        return q

    def parse_drop_table(self, tree: ParserRuleContext, dmltype: str) -> Statement:

        """
        Parse target table from DROP TABLE statement.

        :param tree: AST object parsed
        :param dmltype: DML statement type is passed for Query object
        instantiation
        :return: Query object containing the statement information
        """

        q = Statement(operation=dmltype)
        target = self.parse_object_name(tree.tables().getText().lower())
        q.target_table = Table(name=target[1], schema=target[0])
        return q

    def parse_update(self, tree: ParserRuleContext, dmltype: str) \
            -> Optional[Statement]:

        """
        Parses target table, source table(s) and target columns from
        an UPDATE statement.

        :param tree: AST object parsed
        :param dmltype: DML statement type is passed for Query object
        instantiation
        :return: Query object containing the statement information
        """

        q = Statement(operation=dmltype)

        q.target_table = self.get_target_table(tree)
        q.join_table = self.get_source_tables_update(tree)
        q.target_columns = self.get_updated_columns(tree)

        # TODO -> Get rid of this if statement
        if q.target_table and q.join_table:
            return q

    def get_inserted_tables(self, tree: ParserRuleContext) \
            -> Tuple[List[Table], List[Table]]:

        """
        Gets all source tables from an INSERT statement.

        :param tree: AST object parsed
        :return: list of source tables names string
        """

        for child in tree.getChildren():
            if isinstance(child, MySqlParser.InsertStatementValueContext):
                from_table = self.get_source_tables_insert(child, 'from')
                join_table = self.get_source_tables_insert(child, 'join')
                return from_table, join_table

    def parse_insert(self, tree: ParserRuleContext, dmltype: str) -> Statement:

        """
        Parses target table, source table(s) and target columns from
        an INSERT statement.

        :param tree: AST object parsed
        :param dmltype: DML statement type for Query object instantiation
        :return: Query object containing the statement information
        """

        q = Statement(operation=dmltype)
        q.target_table = self.get_target_table(tree)
        q.from_table, q.join_table = self.get_inserted_tables(tree)
        q.target_columns = self.get_inserted_columns(tree)

        return q

    def get_delete_table(self, tree: ParserRuleContext) \
            -> Optional[List[Table]]:

        """
        Gets the table name from a DELETE statement.

        :param tree: AST object parsed
        :return: the target table name
        """

        for child in tree.getChildren():
            if isinstance(child, MySqlParser.DeleteStatementValueContext):
                return self.get_source_tables_insert(child, 'from')

    def parse_delete(self, tree: ParserRuleContext, dmltype: str) -> Statement:

        """
        Parses target table name from a DELETE statement.

        :param tree: AST object parsed
        :param dmltype: DML statement type for Query object instantiation
        :return: Query object containing the statement information
        """

        q = Statement(operation=dmltype)
        q.target_table = self.get_target_table(tree)

        return q

    def get_source_tables_update(self, tree: ParserRuleContext) \
            -> List[Table]:

        """
        Collects recursively table names in JOIN clauses of an
        update statement.

        :param tree: AST object parsed
        :return: list of source tables
        """

        tables = []

        for c in tree.getChildren():
            if isinstance(c, MySqlParser.JoinPartContext):
                tables.extend(self.get_all_tables(c))
            elif not (isinstance(c, TerminalNode) or isinstance(c, ErrorNode)):
                tables.extend(self.get_source_tables_update(c))

        return tables

    def get_source_tables_insert(self, tree: ParserRuleContext, clause: str) \
            -> List[Table]:

        """
        Collects recursively table names in FROM and JOIN clauses in
        insert/replace statement.

        :param tree: AST object parsed
        :param clause: clause type, must be one of ('from', 'join')
        :return: list of source tables
        """

        assert clause in ('from', 'join'), f'variable clause must be one of ' \
                                           f'(from, join)'

        tables = []

        for c in tree.getChildren():
            if isinstance(c, MySqlParser.FromClauseContext):
                froms = c.tableSources()
                for i in froms.tableSource():
                    if clause == 'from':
                        f = i.tableSourceItem()
                        tables.extend(self.get_all_tables(f))
                    else:
                        f = i.joinPart()
                        for x in f:
                            tables.extend(self.get_all_tables(x))
            elif not (isinstance(c, TerminalNode) or isinstance(c, ErrorNode)):
                tables.extend(self.get_source_tables_insert(c, clause))
        return tables

    def get_target_table(self, tree: ParserRuleContext) -> Table:

        """
        Walks recursively to the first table name found in a statement AST
        and returns it.

        :param tree: AST object parsed
        :return: Table object
        """

        for c in tree.getChildren():

            if isinstance(c, MySqlParser.TableNameContext):
                schema, name = self.parse_object_name(c.getText().lower())
                t = Table(name, schema)
                return t
            elif not (isinstance(c, TerminalNode) or isinstance(c, ErrorNode)):
                return self.get_target_table(c)

    def get_all_tables(self, tree: ParserRuleContext) -> List[Table]:

        """
        Gets all table names inside a tree, appends them to a list of
        table names and finally returns the list.

        :param tree: AST object parsed
        :return: list of table names
        """

        tables = []
        for c in tree.getChildren():
            if isinstance(c, MySqlParser.TableNameContext):
                schema, name = self.parse_object_name(c.getText().lower())
                t = Table(name, schema)
                tables.append(t)
            elif isinstance(c, MySqlParser.QueryExpressionContext):
                c = c.querySpecification()
                tables.extend(self.get_all_tables(c))
            elif not (isinstance(c, TerminalNode) or isinstance(c, ErrorNode)):
                tables.extend(self.get_all_tables(c))
        return tables
