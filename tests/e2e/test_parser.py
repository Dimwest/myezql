import pytest
from tests.utils import *
from parse.runner import Runner


@pytest.mark.parametrize(
    "delimiter, mode, path, expected",
    [(';', 'ddl', delete_path, [PARSE_FILE_DELETE_EXPECTED]),
     (';', 'ddl', update_path, [PARSE_FILE_UPDATE_EXPECTED]),
     (';', 'ddl', insert_path, [PARSE_FILE_INSERT_EXPECTED]),
     (';', 'ddl', replace_path, [PARSE_FILE_REPLACE_EXPECTED]),
     (';', 'ddl', truncate_path, [PARSE_FILE_TRUNCATE_EXPECTED]),
     (';', 'ddl', drop_table_path, [PARSE_FILE_DROP_TABLE_EXPECTED]),
     (';', 'ddl', create_table_query_path, [PARSE_FILE_CREATE_TABLE_QUERY_EXPECTED]),
     (';', 'ddl', create_table_columns_path, [PARSE_FILE_CREATE_TABLE_COLUMNS_EXPECTED]),
     (';', 'ddl', create_table_like_path, [PARSE_FILE_CREATE_TABLE_LIKE_EXPECTED])]
)
def test_run_file(delimiter, mode, path, expected):

    """
    Test core Run(path) function of the parser component and ensure results are correct.

    :param delimiter: delimiter setting for parsing
    :param mode: parsing mode
    :param path: path to the file/directory to parse
    :param expected: expected results
    """

    p = Runner(TEST_DEFAULT_SCHEMA, delimiter, mode)
    p.run(path)
    assert len(p.results) == len(expected)
    for r in p.results:
        assert r in expected

@pytest.mark.parametrize(
    "delimiter, mode, path, expected",
    [(';', 'ddl', test_dir_path, PARSE_DIR_EXPECTED_DDL),
     (';;', 'procedure', test_dir_path, PARSE_DIR_EXPECTED_PROC)]
)
def test_run_dir(delimiter, mode, path, expected):

    p = Runner(TEST_DEFAULT_SCHEMA, delimiter, mode)
    p.run(path)

    statements = [s for file in p.results for s in file['statements']]
    statements_expected = [s for file in expected for s in file['statements']]

    # Assert statements parsed are correct
    assert sorted(statements, key=lambda k: k['operation'] + k['procedure']) == \
        sorted(statements_expected, key=lambda k: k['operation'] + k['procedure'])
