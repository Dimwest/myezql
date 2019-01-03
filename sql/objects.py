
class Procedure:

    def __init__(self, path, name=None, schema=None, queries=None):

        self.name = name
        self.schema = schema
        self.path = path
        self.queries = queries


class Query:

    def __init__(self,
                 procedure=None,
                 operation=None,
                 target_table=None,
                 target_columns=None,
                 from_table=None,
                 join_table=None):

        # Parent procedure
        self.procedure = procedure

        # Parsed attributes
        self.operation = operation
        self.from_table = from_table
        self.join_table = join_table
        self.target_table = target_table
        self.target_columns = target_columns


class Table:

    def __init__(self, name, schema):

        self.name = name
        self.schema = schema
