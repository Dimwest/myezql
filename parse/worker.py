import os
import re
import multiprocessing as mp
from parse.regex import procedure_regex, NAME_REGEX
from sqlparse import format as fmt
from antlr4 import ParserRuleContext, TerminalNode, ErrorNode, \
    InputStream, CommonTokenStream
from parse.lexer import MySqlLexer
from parse.parser import MySqlParser
from parse.mapper import Mapper
from typing import List, Tuple, Optional, Dict
from utils.processing import flatten, merge_results
from copy import deepcopy


class Worker:

    """Core object managing all the parsing operations using ANTLR4-generated parser"""

    def __init__(self, default_schema: str, delimiter: str, pmode: str, fmode: str) -> None:

        self.results = []
        self.delimiter = delimiter
        self.proc_regex = procedure_regex(self.delimiter)
        self.default_schema = default_schema
        self.pmode = pmode
        self.fmode = fmode

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
                    sql_files.append(f'{root}/{name}'.replace('//', '/'))
        results = pool.map(self.parse_file, sql_files)
        self.results = [p for file in results for p in file]

    def parse_file(self, path: str) -> List[Dict]:

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
            if self.pmode == 'procedure':
                procedures = re.findall(self.proc_regex, file_input)
                for proc in procedures:
                    results.append(self.parse_str(path, proc))
            elif self.pmode == 'ddl':
                results.append(self.parse_str(path, file_input))

        return results

    def parse_str(self, path: str, p: str) -> Dict:

        """
        Gets all configured DDL statements inside a procedure body,
        parses them, stores results in Procedure objects, and appends
        these objects to self.results.

        :param path: the procedure path is passed here as the Procedure
        instantiation requires it.
        :param p: procedure body string
        :param pmode: parsing mode, can be "procedure" or "ddl"
        """

        if self.pmode == 'procedure':
            schema, name = self.get_procedure_name(p)
        else:
            schema, name = '', path

        proc = {'schema': schema,
                'name': name,
                'path': path,
                'statements': []}

        mapper = Mapper(self.delimiter, self.pmode)

        for ddl_type in mapper.extract_regexes.keys():
            statements = re.findall(mapper.extract_regexes[ddl_type], p)
            for s in statements:
                q = self.parse_statement(ddl_type, s, mapper)
                if q:
                    q['procedure'] = name
                    proc['statements'].append(q)

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

    def parse_statement(self, ddl_type: str, s: str, mapper: Mapper) -> Dict:

        """
        Cleans DDL statement, creates parsing objects, and returns a
        Query object.

        :param ddl_type: type of DDL statement being parsed
        :param s: DDL statement string
        :param mapper: Mapper object
        :return: Query object containing the statement information
        """

        input_stream = InputStream(s)
        lexer = MySqlLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = MySqlParser(token_stream)
        mapper.parser = parser
        mapper.map_methods(self)
        tree = mapper.mapper[ddl_type]['parsermethod']()
        r = mapper.mapper[ddl_type]['extractor'](tree, ddl_type)
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

    def parse_create_table(self, tree: ParserRuleContext, ddl_type: str) \
            -> Dict:

        """
        Parse the three types of CREATE TABLE statements existing in MySQL 5.6,
        returns as much information as possible in each case.

        :param tree: AST object parsed
        :param ddl_type: DDL statement type for Query object instantiation
        :return: Query object containing the statement information
        """

        q = dict()
        q['target_table'] = self.get_target_table(tree)

        # Parse create table column statements
        if isinstance(tree, MySqlParser.ColumnCreateTableContext):
            q['operation'] = f'{ddl_type} COLUMNS'
            q['target_columns'] = self.get_create_table_columns(tree)

        # Parse create table query statements
        elif isinstance(tree, MySqlParser.QueryCreateTableContext):
            q['operation'] = f'{ddl_type} QUERY'
            q['from_table'] = self.get_source_tables_insert(tree, 'from')
            q['join_table'] = self.get_source_tables_insert(tree, 'join')
            try:
                query = tree.selectStatement().querySpecification()
            except AttributeError as e:
                query = tree.selectStatement().queryExpression().querySpecification()
            q['target_columns'] = query.selectElements().getText().lower().split(',')

        # Parse create table like statements
        elif isinstance(tree, MySqlParser.CopyCreateTableContext):
            q['operation'] = f'{ddl_type} LIKE'
            target = self.parse_object_name(tree.tableName(0).getText().lower())
            q['target_table'] = {'schema': target[0], 'name': target[1]}
            source = self.parse_object_name(tree.tableName(1).getText().lower())
            q['from_table'] = [{'schema': source[0], 'name': source[1]}]

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

    def parse_truncate(self, tree: ParserRuleContext, ddl_type: str) -> Dict:

        """
        Parse target table from TRUNCATE statement.

        :param tree: AST object parsed
        :param ddl_type: DDL statement type is passed for Query object
        instantiation
        :return: Query object containing the statement information
        """

        q = {'operation': ddl_type,
             'target_table': self.get_target_table(tree)}
        return q

    def parse_drop_table(self, tree: ParserRuleContext, ddl_type: str) -> Dict:

        """
        Parse target table from DROP TABLE statement.

        :param tree: AST object parsed
        :param ddl_type: DDL statement type is passed for Query object
        instantiation
        :return: Query object containing the statement information
        """

        q = {'operation': ddl_type}
        target = self.parse_object_name(tree.tables().getText().lower())
        q['target_table'] = {'name': target[1], 'schema': target[0]}
        return q

    def parse_update(self, tree: ParserRuleContext, ddl_type: str) \
            -> Optional[Dict]:

        """
        Parses target table, source table(s) and target columns from
        an UPDATE statement.

        :param tree: AST object parsed
        :param ddl_type: DDL statement type is passed for Query object
        instantiation
        :return: Query object containing the statement information
        """

        q = {'operation': ddl_type,
             'target_table': self.get_target_table(tree),
             'join_table': self.get_source_tables_update(tree),
             'target_columns': self.get_updated_columns(tree)}

        # TODO -> Get rid of this if statement
        if q['target_table'] and q['join_table']:
            return q

    def get_inserted_tables(self, tree: ParserRuleContext) \
            -> Tuple[List[Dict], List[Dict]]:

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

    def parse_insert(self, tree: ParserRuleContext, ddl_type: str) -> Dict:

        """
        Parses target table, source table(s) and target columns from
        an INSERT statement.

        :param tree: AST object parsed
        :param ddl_type: DDL statement type for Query object instantiation
        :return: Query object containing the statement information
        """

        from_table, join_table = self.get_inserted_tables(tree)
        q = {'operation': ddl_type,
             'target_table': self.get_target_table(tree),
             'from_table': from_table,
             'join_table': join_table,
             'target_columns': self.get_inserted_columns(tree)}

        return q

    def get_delete_table(self, tree: ParserRuleContext) \
            -> Optional[List[Dict]]:

        """
        Gets the table name from a DELETE statement.

        :param tree: AST object parsed
        :return: the target table name
        """

        for child in tree.getChildren():
            if isinstance(child, MySqlParser.DeleteStatementValueContext):
                return self.get_source_tables_insert(child, 'from')

    def parse_delete(self, tree: ParserRuleContext, ddl_type: str) -> Dict:

        """
        Parses target table name from a DELETE statement.

        :param tree: AST object parsed
        :param ddl_type: DDL statement type for Query object instantiation
        :return: Query object containing the statement information
        """

        q = {'operation': ddl_type,
             'target_table': self.get_target_table(tree)}

        return q

    def get_source_tables_update(self, tree: ParserRuleContext) \
            -> List[Dict]:

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
            -> List[Dict]:

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

    def get_target_table(self, tree: ParserRuleContext) -> Dict:

        """
        Walks recursively to the first table name found in a statement AST
        and returns it.

        :param tree: AST object parsed
        :return: Table object
        """

        for c in tree.getChildren():

            if isinstance(c, MySqlParser.TableNameContext):
                schema, name = self.parse_object_name(c.getText().lower())
                t = {'schema': schema, 'name': name}
                return t
            elif not (isinstance(c, TerminalNode) or isinstance(c, ErrorNode)):
                return self.get_target_table(c)

    def get_all_tables(self, tree: ParserRuleContext) -> List[Dict]:

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
                t = {'schema': schema, 'name': name}
                tables.append(t)
            elif isinstance(c, MySqlParser.QueryExpressionContext):
                c = c.querySpecification()
                tables.extend(self.get_all_tables(c))
            elif not (isinstance(c, TerminalNode) or isinstance(c, ErrorNode)):
                tables.extend(self.get_all_tables(c))
        return tables

    def tables_filter(self, tables: List[Dict]) -> None:

        """
        Filters statements based on list of tables and filtering mode set for
        the worker.

        :param tables: list of tables to filter on
        """

        if self.fmode == 'simple':
            self.simple_filter(tables)
        elif self.fmode == 'rec':
            self.recursive_filter(tables)

    def simple_filter(self, tables: List[Dict]) -> None:

        """
        Filters statements based on a list of tables: only statements containing
        direct parents/children of the selected tables will be kept in results.

        :param tables: list of table dictionaries with keys "schema" and "name"
        """

        for p in self.results:
            p['statements'] = [s for s in p['statements']
                               if any(t in s['from_table'] for t in tables if s.get('from_table'))
                               or any(t in s['join_table'] for t in tables if s.get('join_table'))
                               or any(t == s['target_table'] for t in tables)]

    def recursive_filter_parents(self, tables: List[Dict], parents_done: List[Dict]=None) -> List[Dict]:

        """
        Recursively filters statements containing all parent tables relating to the list
        of specified tables.

        :param tables: list of tables which parents have to be filtered
        :param parents_done: list of parent tables already fetched, to avoid infinite recursion
        :return: filtered list of procedure/file dictionaries
        """

        filtered_results = []
        results = deepcopy(self.results)

        # For all procedures/files in results
        for p in results:

            # Filter only statements which contain one of the filtered tables as target
            p['statements'] = [s for s in p['statements']
                               if any(t == s['target_table'] for t in tables)]

            # Add this filtered procedure/file to results
            filtered_results.append(p)

            # Get parent (source) tables in these statements
            parents = [s['from_table'] for s in p['statements'] if s.get('from_table')]
            parents.extend([s['join_table'] for s in p['statements'] if s.get('join_table')])
            parents = flatten(parents)

            if parents_done:
                parents = [x for x in parents if x not in parents_done]
            else:
                parents_done = []

            parents_done.extend(parents)

            # Repeat the operation for the parent tables if any
            if parents:
                filtered_results.extend(self.recursive_filter_parents(parents, parents_done))

        return filtered_results

    def recursive_filter_children(self, tables: List[Dict], children_done: List[Dict]=None) -> List[Dict]:

        """
        Recursively filters statements containing all child tables relating to the list
        of specified tables.

        :param tables: list of tables which parents have to be filtered
        :param children_done: list of child tables already fetched, to avoid infinite recursion
        :return: filtered list of procedure/file dictionaries
        """

        filtered_results = []
        results = deepcopy(self.results)

        # For all procedures/files in results
        for p in results:

            # Filter only statements which contain one of the filtered tables as source
            p['statements'] = [s for s in p['statements']
                               if any(t in s['from_table'] for t in tables if s.get('from_table'))
                               or any(t in s['join_table'] for t in tables if s.get('join_table'))]

            # Add this filtered procedure/file to results
            filtered_results.append(p)

            # Get children (target) tables in these statements
            children = [s['target_table'] for s in p['statements']]

            if children_done:
                children = [x for x in children if x not in children_done]
            else:
                children_done = []

            children_done.extend(children)

            # Repeat the operation for the parent tables if any
            if children:
                filtered_results.extend(self.recursive_filter_children(children, children_done))

        return filtered_results

    def recursive_filter(self, tables: List[Dict]) -> None:

        """
        Recursively filters parent and children tables relating to a
        list of specified tables.

        :param tables: list of table dictionaries to filter on
        """

        results = self.recursive_filter_parents(tables)
        results += self.recursive_filter_children(tables)
        self.results = merge_results(results)
