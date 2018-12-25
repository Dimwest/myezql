
class Procedure:

    def __init__(self, path, name=None, schema=None):

        self.name = name
        self.schema = schema
        self.path = path
        self.queries = []


class Query:

    def __init__(self,
                 procedure=None,
                 type=None,
                 operation=None,
                 target_table=None,
                 target_columns=None,
                 from_table=None,
                 where=None,
                 group_by=None,
                 having=None,
                 tokens=None,
                 tree=None,
                 text=None):

        # Parent procedure
        self.procedure = procedure

        # Type attributes
        self.type = type

        # Parsed attributes
        self.operation = operation
        self.from_table = from_table
        self.target_table = target_table
        self.target_columns = target_columns
        self.where = where
        self.group_by = group_by
        self.having = having
        self.tokens = tokens
        self.tree = tree
        self.text = text


class Table:

    def __init__(self, name, schema):

        self.name = name
        self.schema = schema


