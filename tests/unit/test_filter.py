from parse.worker import Worker
from tests.utils import TEST_DEFAULT_SCHEMA, TEST_DELIMITER, TEST_MODE, \
    FILTER_TEST_INPUT, SIMPLE_FILTER_EXPECTED, RECURSIVE_FILTER_EXPECTED
from copy import deepcopy


def test_procedure_filter():

    """
    Ensure that procedure filter works as expected, keeping only procedures selected for
    filtering.
    """

    p = Worker(TEST_DEFAULT_SCHEMA, TEST_DELIMITER, TEST_MODE, 'simple')
    p.results = deepcopy(FILTER_TEST_INPUT)
    p.procedures_filter([
        {'schema': FILTER_TEST_INPUT[0]['schema'],
         'name': FILTER_TEST_INPUT[0]['name']}
    ])
    assert p.results == FILTER_TEST_INPUT

    p.procedures_filter([
        {'schema': 'another_schema',
         'name': 'another_name'}
    ])
    assert p.results == []


def test_simple_filter():

    """
    Ensure that simple filter works as expected, keeping only direct parents/children of
    the selected table(s).
    """

    p = Worker(TEST_DEFAULT_SCHEMA, TEST_DELIMITER, TEST_MODE, None)
    p.results = deepcopy(FILTER_TEST_INPUT)
    p.simple_filter([{'schema': 'default_schema', 'name': 'test_table_1'}])
    assert p.results == SIMPLE_FILTER_EXPECTED


def test_recursive_filter():

    """
    Ensure that recursive filter works as expected, getting all indirect parents/children
    of the selected table(s)
    """

    p = Worker(TEST_DEFAULT_SCHEMA, TEST_DELIMITER, TEST_MODE, None)
    p.results = deepcopy(FILTER_TEST_INPUT)
    p.recursive_filter([{'schema': 'default_schema', 'name': 'test_table_1'}])
    assert p.results == RECURSIVE_FILTER_EXPECTED
