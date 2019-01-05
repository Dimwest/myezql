import os
from sqlparse import format as fmt
from sql.objects import Procedure
from utils.extract import *


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
        Walks through a given directory, parses SQL procedures in all SQL
        files found, appends Procedure objects to self.results.

        :param dir_path: path to the target directory
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

        with open(path, 'r') as file:
            # Grammar is case-sensitive. Input has to be converted
            # to upper case before parsing
            input = fmt(file.read().upper(), strip_comments=True).strip()

            # Find all CREATE PROCEDURE statements and parse them
            procedures = re.findall(PROCEDURE_REGEX, input)
            for proc in procedures:
                self.parse_procedure(path, proc)

    def parse_procedure(self, path: str, p: str) -> None:

        """
        Gets all configured DML statements inside a procedure body,
        parses them, stores results in Procedure objects, and appends
        these objects to self.results.

        :param path: the procedure path is passed here as the Procedure
        instantiation requires it.
        :param p: procedure body string
        """

        schema, name = get_procedure_name(p)
        proc = Procedure(path, name=name, schema=schema, queries=[])

        mapper = Mapper()

        for dmltype in mapper.extract_regexes.keys():
            statements = re.findall(mapper.extract_regexes[dmltype], p)
            for s in statements:
                q = parse_statement(dmltype, s, mapper)
                if q:
                    q.procedure = name
                    proc.queries.append(q)

        self.results.append(proc)
