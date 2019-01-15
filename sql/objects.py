
class Procedure:

    def __init__(self, path, name=None, schema=None, statements=None):

        self.name = name
        self.schema = schema
        self.path = path
        self.statements = statements

    def __eq__(self, other):

        if isinstance(other, Procedure):
            return (self.name == other.name
                    and self.schema == other.schema
                    and self.path == other.path
                    and self.statements == other.statements)

        return False


class Statement:

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

    def __eq__(self, other):

        if isinstance(other, Statement):

            return (self.procedure == other.procedure
                    and self.operation == other.operation
                    and self.from_table == other.from_table
                    and self.join_table == other.join_table
                    and self.target_table == other.target_table
                    and self.target_columns == other.target_columns)

        return False


class Table:

    def __init__(self, name, schema):

        self.name = name
        self.schema = schema

    def __eq__(self, other):

        if isinstance(other, Table):
            return self.name == other.name and self.schema == other.schema

        return False
