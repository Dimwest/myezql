from sqlparse import format as fmt

test_dir_path = './tests/_resources/'
procedure_path = './tests/_resources/procedure.sql'
insert_path = './tests/_resources/insert.sql'
update_path = './tests/_resources/update.sql'
delete_path = './tests/_resources/delete.sql'
truncate_path = './tests/_resources/truncate.sql'

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

# Open and upper case test truncate statement
with open(truncate_path, 'r') as file:
    TEST_TRUNCATE_STATEMENT = fmt(file.read().upper(), strip_comments=True).strip()

# test default parameters
TEST_DEFAULT_SCHEMA = 'default_schema'
TEST_DELIMITER = ';;'
TEST_MODE = 'procedure'

# Define parse_statement results

PARSE_STATEMENT_INSERT_EXPECTED = {'operation': 'INSERT',
                                   'from_table': [{'schema': TEST_DEFAULT_SCHEMA, 'name': 'src_tab_1'}],
                                   'join_table': [
                                       {'schema': TEST_DEFAULT_SCHEMA, 'name': 'src_tab_2'},
                                       {'schema': TEST_DEFAULT_SCHEMA, 'name': 'src_tab_3'}
                                   ],
                                   'target_table': {'schema': TEST_DEFAULT_SCHEMA, 'name': 'mytable'},
                                   'target_columns': ['col_1', 'col_2', 'col_3', 'col_4', 'col_5', 'col_6', 'col_7']}


PARSE_STATEMENT_UPDATE_EXPECTED = {'operation': 'UPDATE',
                                   'join_table': [
                                       {'schema': TEST_DEFAULT_SCHEMA, 'name': 'src_tab_9'},
                                   ],
                                   'target_table': {'schema': TEST_DEFAULT_SCHEMA, 'name': 'src_tab_8'},
                                   'target_columns': ['tab_8.col_3=tab_9.col4', 'tab_8.col_4=tab_9.col5']}

PARSE_STATEMENT_DELETE_EXPECTED = {'operation': 'DELETE',
                                   'target_table': {'schema': TEST_DEFAULT_SCHEMA, 'name': 'src_tab_10'}}

PARSE_STATEMENT_TRUNCATE_EXPECTED = {'operation': 'TRUNCATE',
                                     'target_table': {'schema': TEST_DEFAULT_SCHEMA, 'name': 'src_tab_11'}}

# Define parse_file result components for procedure mode

INSERT_EXPECTED = {'operation': 'INSERT',
                   'procedure': 'testproc',
                   'from_table': [{'schema': TEST_DEFAULT_SCHEMA, 'name': 'src_tab_1'}],
                   'join_table': [
                       {'schema': TEST_DEFAULT_SCHEMA, 'name': 'src_tab_2'},
                       {'schema': TEST_DEFAULT_SCHEMA, 'name': 'src_tab_3'}
                   ],
                   'target_table': {'schema': TEST_DEFAULT_SCHEMA, 'name': 'mytable'},
                   'target_columns': ['col_1', 'col_2', 'col_3', 'col_4', 'col_5', 'col_6', 'col_7']}

UPDATE_EXPECTED = {'operation': 'UPDATE',
                   'procedure': 'testproc',
                   'join_table': [
                       {'schema': TEST_DEFAULT_SCHEMA, 'name': 'src_tab_9'},
                   ],
                   'target_table': {'schema': TEST_DEFAULT_SCHEMA, 'name': 'src_tab_8'},
                   'target_columns': ['tab_8.col_3=tab_9.col4', 'tab_8.col_4=tab_9.col5']}

DELETE_EXPECTED = {'operation': 'DELETE',
                   'procedure': 'testproc',
                   'target_table': {'schema': TEST_DEFAULT_SCHEMA, 'name': 'src_tab_10'}}

TRUNCATE_EXPECTED = {'operation': 'TRUNCATE',
                     'procedure': 'testproc',
                     'target_table': {'schema': TEST_DEFAULT_SCHEMA, 'name': 'src_tab_11'}}

# Define parse_file results for procedure mode

PARSE_FILE_PROCEDURE_EXPECTED = {'path': procedure_path,
                                 'name': 'testproc',
                                 'schema': 'example',
                                 'statements': [INSERT_EXPECTED,
                                                UPDATE_EXPECTED,
                                                DELETE_EXPECTED,
                                                TRUNCATE_EXPECTED]}

# Define parse_file results for ddl mode

PARSE_FILE_DELETE_EXPECTED = {'path': delete_path,
                              'name': delete_path,
                              'schema': '',
                              'statements': [
                                  {'procedure': delete_path,
                                   'operation': 'DELETE',
                                   'target_table': {
                                       'name': 'src_tab_10',
                                       'schema': TEST_DEFAULT_SCHEMA
                                   }}
                              ]}


PARSE_FILE_TRUNCATE_EXPECTED = {'path': truncate_path,
                                'name': truncate_path,
                                'schema': '',
                                'statements': [
                                    {'procedure': truncate_path,
                                     'operation': 'TRUNCATE',
                                     'target_table': {
                                         'name': 'src_tab_11',
                                         'schema': TEST_DEFAULT_SCHEMA
                                     }}
                                ]}


PARSE_FILE_INSERT_EXPECTED = {'path': insert_path,
                              'name': insert_path,
                              'schema': '',
                              'statements': [
                                  {'operation': 'INSERT',
                                   'procedure': insert_path,
                                   'from_table': [{'schema': TEST_DEFAULT_SCHEMA, 'name': 'src_tab_1'}],
                                   'join_table': [
                                       {'schema': TEST_DEFAULT_SCHEMA, 'name': 'src_tab_2'},
                                       {'schema': TEST_DEFAULT_SCHEMA, 'name': 'src_tab_3'}
                                   ],
                                   'target_table': {'schema': TEST_DEFAULT_SCHEMA, 'name': 'mytable'},
                                   'target_columns': ['col_1', 'col_2', 'col_3', 'col_4', 'col_5', 'col_6', 'col_7']}
                              ]}


PARSE_FILE_UPDATE_EXPECTED = {'path': update_path,
                              'name': update_path,
                              'schema': '',
                              'statements': [
                                  {'operation': 'UPDATE',
                                   'procedure': update_path,
                                   'join_table': [
                                       {'schema': TEST_DEFAULT_SCHEMA, 'name': 'src_tab_9'},
                                   ],
                                   'target_table': {'schema': TEST_DEFAULT_SCHEMA, 'name': 'src_tab_8'},
                                   'target_columns': ['tab_8.col_3=tab_9.col4', 'tab_8.col_4=tab_9.col5']}
                              ]}


# Define parse_dir results for ddl mode

DIR_PROCEDURE_EXPECTED_INSERT = {'operation': 'INSERT',
                                 'procedure': procedure_path,
                                 'from_table': [{'schema': TEST_DEFAULT_SCHEMA, 'name': 'src_tab_1'}],
                                 'join_table': [
                                     {'schema': TEST_DEFAULT_SCHEMA, 'name': 'src_tab_2'},
                                     {'schema': TEST_DEFAULT_SCHEMA, 'name': 'src_tab_3'}
                                 ],
                                 'target_table': {'schema': TEST_DEFAULT_SCHEMA, 'name': 'mytable'},
                                 'target_columns': ['col_1', 'col_2', 'col_3', 'col_4', 'col_5', 'col_6', 'col_7']}

DIR_PROCEDURE_EXPECTED_UPDATE = {'operation': 'UPDATE',
                                 'procedure': procedure_path,
                                 'join_table': [
                                     {'schema': TEST_DEFAULT_SCHEMA, 'name': 'src_tab_9'},
                                 ],
                                 'target_table': {'schema': TEST_DEFAULT_SCHEMA, 'name': 'src_tab_8'},
                                 'target_columns': ['tab_8.col_3=tab_9.col4', 'tab_8.col_4=tab_9.col5']}

DIR_PROCEDURE_EXPECTED_DELETE = {'operation': 'DELETE',
                                 'procedure': procedure_path,
                                 'target_table': {'schema': TEST_DEFAULT_SCHEMA, 'name': 'src_tab_10'}}

DIR_PROCEDURE_EXPECTED_TRUNCATE = {'operation': 'TRUNCATE',
                                   'procedure': procedure_path,
                                   'target_table': {'schema': TEST_DEFAULT_SCHEMA, 'name': 'src_tab_11'}}

DIR_PROCEDURE_EXPECTED = {'path': procedure_path,
                          'name': procedure_path,
                          'schema': '',
                          'statements': [
                              DIR_PROCEDURE_EXPECTED_INSERT,
                              DIR_PROCEDURE_EXPECTED_UPDATE,
                              DIR_PROCEDURE_EXPECTED_DELETE,
                              DIR_PROCEDURE_EXPECTED_TRUNCATE
                          ]}


PARSE_DIR_EXPECTED_DDL = [
    PARSE_FILE_TRUNCATE_EXPECTED,
    PARSE_FILE_DELETE_EXPECTED,
    PARSE_FILE_INSERT_EXPECTED,
    DIR_PROCEDURE_EXPECTED,
    PARSE_FILE_UPDATE_EXPECTED
]

# Define parse_dir results for procedure mode

PARSE_DIR_EXPECTED_PROC = [PARSE_FILE_PROCEDURE_EXPECTED]
