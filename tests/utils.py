from sql.objects import Procedure, Statement, Table
from sqlparse import format as fmt

test_dir_path = './tests/_resources/'
procedure_path = './tests/_resources/procedure.sql'
insert_path = './tests/_resources/insert.sql'
update_path = './tests/_resources/update.sql'
delete_path = './tests/_resources/delete.sql'

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

# Test default parameters
TEST_DEFAULT_SCHEMA = 'default_schema'
TEST_DELIMITER = ';;'
TEST_MODE = 'procedure'

PARSE_STATEMENT_INSERT_EXPECTED = Statement(procedure=None,
                                            operation='INSERT',
                                            from_table=[Table(name='src_tab_1', schema=TEST_DEFAULT_SCHEMA)],
                                            join_table=[Table(name='src_tab_2', schema=TEST_DEFAULT_SCHEMA),
                                                  Table(name='src_tab_3', schema=TEST_DEFAULT_SCHEMA)],
                                            target_table=Table(name='mytable', schema=TEST_DEFAULT_SCHEMA),
                                            target_columns=['col_1', 'col_2', 'col_3', 'col_4', 'col_5', 'col_6', 'col_7'])

PARSE_STATEMENT_UPDATE_EXPECTED = Statement(procedure=None,
                                            operation='UPDATE',
                                            join_table=[Table(name='src_tab_9', schema=TEST_DEFAULT_SCHEMA)],
                                            target_table=Table(name='src_tab_8', schema=TEST_DEFAULT_SCHEMA),
                                            target_columns=['tab_8.col_3=tab_9.col4', 'tab_8.col_4=tab_9.col5'])

PARSE_STATEMENT_DELETE_EXPECTED = Statement(procedure=None,
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


PARSE_FILE_PROCEDURE_EXPECTED = Procedure(path=procedure_path,
                                          name='testproc',
                                          schema='example',
                                          statements=[INSERT_EXPECTED, UPDATE_EXPECTED, DELETE_EXPECTED])


PARSE_FILE_DELETE_EXPECTED = Procedure(path=delete_path, name=delete_path, schema='',
                                       statements=[Statement(
                                     procedure=delete_path,
                                     operation='DELETE',
                                     target_table=Table(name='src_tab_10', schema=TEST_DEFAULT_SCHEMA))])


PARSE_FILE_INSERT_EXPECTED = Procedure(path=insert_path, name=insert_path, schema='',
                                       statements=[
                                     Statement(procedure=insert_path,
                                               operation='INSERT',
                                               from_table=[Table(name='src_tab_1', schema=TEST_DEFAULT_SCHEMA)],
                                               join_table=[Table(name='src_tab_2', schema=TEST_DEFAULT_SCHEMA),
                                                           Table(name='src_tab_3', schema=TEST_DEFAULT_SCHEMA)],
                                               target_table=Table(name='mytable', schema=TEST_DEFAULT_SCHEMA),
                                               target_columns=[
                                                   'col_1', 'col_2', 'col_3', 'col_4', 'col_5', 'col_6', 'col_7'
                                               ]
                                               )
                                 ]
                                       )

PARSE_FILE_UPDATE_EXPECTED = Procedure(path=update_path, name=update_path, schema='',
                                       statements=[
                                     Statement(procedure=update_path,
                                               operation='UPDATE',
                                               join_table=[Table(name='src_tab_9', schema=TEST_DEFAULT_SCHEMA)],
                                               target_table=Table(name='src_tab_8', schema=TEST_DEFAULT_SCHEMA),
                                               target_columns=['tab_8.col_3=tab_9.col4', 'tab_8.col_4=tab_9.col5'])
                                 ]
                                       )

DIR_PROCEDURE_EXPECTED_DELETE = Statement(
    procedure=procedure_path,
    operation='DELETE',
    target_table=Table(name='src_tab_10', schema=TEST_DEFAULT_SCHEMA)
)


DIR_PROCEDURE_EXPECTED_INSERT = Statement(procedure=procedure_path,
                                          operation='INSERT',
                                          from_table=[Table(name='src_tab_1', schema=TEST_DEFAULT_SCHEMA)],
                                          join_table=[Table(name='src_tab_2', schema=TEST_DEFAULT_SCHEMA),
                                                      Table(name='src_tab_3', schema=TEST_DEFAULT_SCHEMA)],
                                          target_table=Table(name='mytable', schema=TEST_DEFAULT_SCHEMA),
                                          target_columns=[
                                              'col_1', 'col_2', 'col_3', 'col_4', 'col_5', 'col_6', 'col_7'
                                          ]
                                          )

DIR_PROCEDURE_EXPECTED_UPDATE = Statement(procedure=procedure_path,
                                          operation='UPDATE',
                                          join_table=[Table(name='src_tab_9', schema=TEST_DEFAULT_SCHEMA)],
                                          target_table=Table(name='src_tab_8', schema=TEST_DEFAULT_SCHEMA),
                                          target_columns=['tab_8.col_3=tab_9.col4', 'tab_8.col_4=tab_9.col5'])

DIR_PROCEDURE_EXPECTED = Procedure(path=procedure_path, name=procedure_path, schema='',
                                   statements=[
                                       DIR_PROCEDURE_EXPECTED_INSERT,
                                       DIR_PROCEDURE_EXPECTED_UPDATE,
                                       DIR_PROCEDURE_EXPECTED_DELETE
                                   ]
                                   )

PARSE_DIR_EXPECTED_DDL = [
    PARSE_FILE_DELETE_EXPECTED,
    PARSE_FILE_INSERT_EXPECTED,
    DIR_PROCEDURE_EXPECTED,
    PARSE_FILE_UPDATE_EXPECTED
]

PARSE_DIR_EXPECTED_PROC = [PARSE_FILE_PROCEDURE_EXPECTED]
