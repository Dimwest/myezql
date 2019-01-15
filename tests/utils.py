from sql.objects import Procedure, Statement, Table
from sqlparse import format as fmt

procedure_path = './tests/resources/procedure.sql'
insert_path = './tests/resources/insert.sql'
update_path = './tests/resources/update.sql'
delete_path = './tests/resources/delete.sql'

# NB: Antlr grammar is case-sensitive. Input has to be upper case.
# Open and upper case test procedure file
with open(procedure_path, 'r') as file:
    TEST_PROCEDURE = fmt(file.read().upper(), strip_comments=True).strip()

# Open and upper case test insert statement
with open(insert_path, 'r') as file:
    TEST_INSERT_STATEMENT = fmt(file.read().upper(), strip_comments=True).strip()

# Open and upper case test update statement
with open(update_path, 'r') as file:
    TEST_UPDATE_STATEMENT = fmt(file.read().upper(), strip_comments=True).strip()

# Open and upper case test delete statement
with open(delete_path, 'r') as file:
    TEST_DELETE_STATEMENT = fmt(file.read().upper(), strip_comments=True).strip()

TEST_DEFAULT_SCHEMA = 'default_schema'
TEST_DELIMITER = ';;'
TEST_MODE = 'procedure'

INSERT_STATEMENT_EXPECTED = Statement(procedure=None,
                                      operation='INSERT',
                                      from_table=[Table(name='src_tab_1', schema=TEST_DEFAULT_SCHEMA)],
                                      join_table=[Table(name='src_tab_2', schema=TEST_DEFAULT_SCHEMA),
                                                  Table(name='src_tab_3', schema=TEST_DEFAULT_SCHEMA)],
                                      target_table=Table(name='mytable', schema=TEST_DEFAULT_SCHEMA),
                                      target_columns=['col_1', 'col_2', 'col_3', 'col_4', 'col_5', 'col_6', 'col_7'])

UPDATE_STATEMENT_EXPECTED = Statement(procedure=None,
                                      operation='UPDATE',
                                      join_table=[Table(name='src_tab_9', schema=TEST_DEFAULT_SCHEMA)],
                                      target_table=Table(name='src_tab_8', schema=TEST_DEFAULT_SCHEMA),
                                      target_columns=['tab_8.col_3=tab_9.col4', 'tab_8.col_4=tab_9.col5'])

DELETE_STATEMENT_EXPECTED = Statement(procedure=None,
                                      operation='DELETE',
                                      target_table=Table(name='src_tab_10', schema=TEST_DEFAULT_SCHEMA))

INSERT_EXPECTED = Statement(procedure='testproc',
                            operation='INSERT',
                            from_table=[Table(name='src_tab_1', schema=TEST_DEFAULT_SCHEMA)],
                            join_table=[Table(name='src_tab_2', schema=TEST_DEFAULT_SCHEMA),
                                    Table(name='src_tab_3', schema=TEST_DEFAULT_SCHEMA)],
                            target_table=Table(name='mytable', schema=TEST_DEFAULT_SCHEMA),
                            target_columns=['col_1', 'col_2', 'col_3', 'col_4', 'col_5', 'col_6', 'col_7'])

UPDATE_EXPECTED = Statement(procedure='testproc',
                            operation='UPDATE',
                            join_table=[Table(name='src_tab_9', schema=TEST_DEFAULT_SCHEMA)],
                            target_table=Table(name='src_tab_8', schema=TEST_DEFAULT_SCHEMA),
                            target_columns=['tab_8.col_3=tab_9.col4', 'tab_8.col_4=tab_9.col5'])

DELETE_EXPECTED = Statement(procedure='testproc',
                            operation='DELETE',
                            target_table=Table(name='src_tab_10', schema=TEST_DEFAULT_SCHEMA))


PROCEDURE_EXPECTED = Procedure(path=procedure_path,
                               name='testproc',
                               schema='example',
                               statements=[INSERT_EXPECTED, UPDATE_EXPECTED, DELETE_EXPECTED])

