import pytest
from tests.utils import *
from parse.runner import Runner
from parse.mapper import Mapper


@pytest.mark.parametrize(
    "delimiter, mode, expected",
    [(';', 'ddl', PARSE_DIR_EXPECTED_DDL),
     (';;', 'procedure', PARSE_DIR_EXPECTED_PROC)]
)
def test_parse_dir(delimiter, mode, expected):

    """
    Ensures that directory parsing works as expected
    """

    # Test directory parsing
    p = Runner(TEST_DEFAULT_SCHEMA, delimiter, mode)
    p.parse_dir(test_dir_path)
    statements = [s for file in p.results for s in file['statements']]
    statements_expected = [s for file in expected for s in file['statements']]

    # Assert statements parsed are correct
    assert sorted(statements, key=lambda k: k['operation'] + k['procedure']) == \
        sorted(statements_expected, key=lambda k: k['operation'] + k['procedure'])


@pytest.mark.parametrize(
    "delimiter, mode, path, expected",
    [(';', 'ddl', delete_path, [PARSE_FILE_DELETE_EXPECTED]),
     (';', 'ddl', update_path, [PARSE_FILE_UPDATE_EXPECTED]),
     (';', 'ddl', insert_path, [PARSE_FILE_INSERT_EXPECTED]),
     (';', 'ddl', replace_path, [PARSE_FILE_REPLACE_EXPECTED]),
     (';', 'ddl', truncate_path, [PARSE_FILE_TRUNCATE_EXPECTED]),
     (';', 'ddl', drop_table_path, [PARSE_FILE_DROP_TABLE_EXPECTED])]
)
def test_parse_file(delimiter, mode, path, expected):

    """
    For each set of args, ensures the parser results are correct.

    :param delimiter: delimiter used for parsing
    :param mode: parsing mode used for parsing
    :param path: path to the file to parse
    :param expected: expected result
    """

    # Ensure file parsing results are correct
    p = Runner(TEST_DEFAULT_SCHEMA, delimiter, mode)
    results = p.parse_file(path)
    assert results == expected


def test_parse_procedure():
    """Run parser on test procedure file and ensure result is correct."""

    # Run parser on test procedure file
    processor = Runner(TEST_DEFAULT_SCHEMA, TEST_DELIMITER, TEST_MODE)
    p = processor.parse_str(procedure_path, TEST_PROCEDURE)

    # Check equality at Procedure level
    assert p['name'] == PARSE_FILE_PROCEDURE_EXPECTED['name']
    assert p['schema'] == PARSE_FILE_PROCEDURE_EXPECTED['schema']
    assert p['path'] == PARSE_FILE_PROCEDURE_EXPECTED['path']
    assert sorted(p['statements'], key=lambda k: k['operation']) == \
        sorted(PARSE_FILE_PROCEDURE_EXPECTED['statements'], key=lambda k: k['operation'])


@pytest.mark.parametrize(
    "test_input, dmltype, expected",
    [(TEST_INSERT_STATEMENT, 'INSERT', PARSE_STATEMENT_INSERT_EXPECTED),
     (TEST_REPLACE_STATEMENT, 'REPLACE', PARSE_STATEMENT_REPLACE_EXPECTED),
     (TEST_UPDATE_STATEMENT, 'UPDATE', PARSE_STATEMENT_UPDATE_EXPECTED),
     (TEST_DELETE_STATEMENT, 'DELETE', PARSE_STATEMENT_DELETE_EXPECTED),
     (TEST_DROP_TABLE_STATEMENT, 'DROP TABLE', PARSE_STATEMENT_DROP_TABLE_EXPECTED),
     (TEST_TRUNCATE_STATEMENT, 'TRUNCATE', PARSE_STATEMENT_TRUNCATE_EXPECTED)]
)
def test_parse_statement(test_input, dmltype, expected):

    """
    Run parser on test statements and ensure results are correct.

    :param test_input: test statement
    :param dmltype: DML type of the statement tested
    :param expected: expected Statement object to compare with parser result
    """

    mapper = Mapper(TEST_DELIMITER, TEST_MODE)
    p = Runner(TEST_DEFAULT_SCHEMA, TEST_DELIMITER, TEST_MODE)
    r = p.parse_statement(dmltype=dmltype, s=test_input, mapper=mapper)
    assert r == expected


def test_parse_object_name():

    """
    Verify that table/procedure string is correctly split into name and schema,
    and that default schema is added when needed.
    """

    # Ensure that object name gets correctly split and default schema behavior works
    p = Runner(TEST_DEFAULT_SCHEMA, TEST_DELIMITER, TEST_MODE)
    assert p.parse_object_name('example.testproc') == ('example', 'testproc')
    assert p.parse_object_name('testproc') == (TEST_DEFAULT_SCHEMA, 'testproc')


def test_get_procedure_name():

    """
    Verify that procedure name is correctly fetched, split into name and schema,
    and that default schema is added when needed.
    """

    # Ensure that procedure name gets correctly identified and split
    p = Runner(TEST_DEFAULT_SCHEMA, TEST_DELIMITER, TEST_MODE)
    assert p.get_procedure_name(TEST_PROCEDURE) == ('example', 'testproc')
