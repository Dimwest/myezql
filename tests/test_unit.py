import pytest
from parse.runner import Runner
from parse.mapper import Mapper
from tests.utils import *


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


def test_equality_check():

    """
    Verify that the __eq__(self, other) method is working as expected for Procedure,
    Statement, and Table objects.
    """

    # Test equality check for procedures
    a = Procedure(path='path', name='name', schema='schema',
                  statements=[
                      Statement(procedure='proc', operation='op', target_table=Table(name='tab1', schema='schema'),
                                target_columns=['col1', 'col2'], from_table=[Table(name='tab2', schema='schema')],
                                join_table=[Table(name='tab2', schema='schema')])])

    b = Procedure(path='path', name='name', schema='schema',
                  statements=[
                      Statement(procedure='proc', operation='op', target_table=Table(name='tab1', schema='schema'),
                                target_columns=['col1', 'col2'], from_table=[Table(name='tab2', schema='schema')],
                                join_table=[Table(name='tab2', schema='schema')])])

    assert a == b

    # Test equality check for statements
    c = Statement(procedure='proc', operation='op', target_table=Table(name='tab1', schema='schema'),
                  target_columns=['col1', 'col2'], from_table=[Table(name='tab2', schema='schema')],
                  join_table=[Table(name='tab2', schema='schema')])

    d = Statement(procedure='proc', operation='op', target_table=Table(name='tab1', schema='schema'),
                  target_columns=['col1', 'col2'], from_table=[Table(name='tab2', schema='schema')],
                  join_table=[Table(name='tab2', schema='schema')])

    assert c == d

    # Test equality check for tables
    e = Table(name='tab1', schema='schema')
    f = Table(name='tab1', schema='schema')

    assert e == f


def test_parse_procedure():
    """Run parser on test procedure file and ensure result is correct."""

    # Run parser on test procedure file
    processor = Runner(TEST_DEFAULT_SCHEMA, TEST_DELIMITER, TEST_MODE)
    p = processor.parse_str(procedure_path, TEST_PROCEDURE)

    # Check equality at Procedure level
    assert p == PROCEDURE_EXPECTED


@pytest.mark.parametrize(
    "test_input, dmltype, expected",
    [(TEST_INSERT_STATEMENT, 'INSERT', INSERT_STATEMENT_EXPECTED),
     (TEST_UPDATE_STATEMENT, 'UPDATE', UPDATE_STATEMENT_EXPECTED),
     (TEST_DELETE_STATEMENT, 'DELETE', DELETE_STATEMENT_EXPECTED)]
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


def test_get_delete_table():
    pass


def test_parse_delete():
    pass


def test_get_source_tables_update():
    pass


def test_get_source_tables_insert():
    pass


def test_get_target_table():
    pass


def test_get_all_tables():
    pass
