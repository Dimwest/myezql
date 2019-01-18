import pytest
from tests.utils import *
from parse.runner import Runner


@pytest.mark.parametrize(
    "delimiter, mode, path, expected",
    [(';', 'ddl', test_dir_path, PARSE_DIR_EXPECTED_DDL),
     (';;', 'procedure', test_dir_path, PARSE_DIR_EXPECTED_PROC),
     (';', 'ddl', delete_path, [PARSE_FILE_DELETE_EXPECTED]),
     (';', 'ddl', update_path, [PARSE_FILE_UPDATE_EXPECTED]),
     (';', 'ddl', insert_path, [PARSE_FILE_INSERT_EXPECTED]),
     (';;', 'procedure', procedure_path, [PARSE_FILE_PROCEDURE_EXPECTED])]
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
    for r in p.results:
        assert r in expected
