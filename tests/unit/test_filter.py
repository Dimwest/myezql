from parse.worker import Worker
from tests.utils import TEST_DEFAULT_SCHEMA, TEST_DELIMITER, TEST_MODE, \
    FILTER_TEST_INPUT, SIMPLE_FILTER_EXPECTED, RECURSIVE_FILTER_EXPECTED
from copy import deepcopy


def test_simple_filter():
    p = Worker(TEST_DEFAULT_SCHEMA, TEST_DELIMITER, TEST_MODE, None)
    p.results = deepcopy(FILTER_TEST_INPUT)
    p.simple_filter([{'schema': 'default_schema', 'name': 'test_table_1'}])
    assert p.results == SIMPLE_FILTER_EXPECTED


def test_recursive_filter():
    p = Worker(TEST_DEFAULT_SCHEMA, TEST_DELIMITER, TEST_MODE, None)
    p.results = deepcopy(FILTER_TEST_INPUT)
    p.recursive_filter([{'schema': 'default_schema', 'name': 'test_table_1'}])
    assert p.results == RECURSIVE_FILTER_EXPECTED
