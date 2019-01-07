from antlrparser.regex import *


class Mapper:

    """Helper class used to map DML extraction regexes with parsing
    methods. Also provides cleanup regexes used to deal with edge
    cases, e.g. table names containing SQL keywords"""

    def __init__(self, delimiter, mode):

        INSERT_REGEX = insert_regex(delimiter) if mode == 'ddl' else insert_regex(';')
        REPLACE_REGEX = replace_regex(delimiter) if mode == 'ddl' else replace_regex(';')
        UPDATE_REGEX = update_regex(delimiter) if mode == 'ddl' else update_regex(';')
        DELETE_REGEX = delete_regex(delimiter) if mode == 'ddl' else delete_regex(';')

        self.extract_regexes = \
            {'INSERT': INSERT_REGEX,
             'REPLACE': REPLACE_REGEX,
             'UPDATE': UPDATE_REGEX,
             'DELETE': DELETE_REGEX}

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

        extractors = \
            {'INSERT': walker.parse_insert,
             'REPLACE': walker.parse_insert,
             'UPDATE': walker.parse_update,
             'DELETE': walker.parse_delete}

        parsermethods = methods
        self.mapper = {k: {'regex': v}
                       for k, v in self.extract_regexes.items()}
        for k in self.mapper.keys():
            self.mapper[k]['parsermethod'] = parsermethods[k]
            self.mapper[k]['extractor'] = extractors[k]
