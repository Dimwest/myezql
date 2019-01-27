import pytest
from parse.regex import *
from tests.utils import *


with open('./tests/_resources/expected/procedure_expected.sql', 'r') as file:
    TEST_PROCEDURE_EXPECTED = fmt(file.read().upper(), strip_comments=True).strip()


@pytest.mark.parametrize(
    "statement, regex_function, expected",
    [(TEST_INSERT_STATEMENT, insert_regex(';'), [TEST_INSERT_STATEMENT]),
     (TEST_REPLACE_STATEMENT, replace_regex(';'), [TEST_REPLACE_STATEMENT]),
     (TEST_DELETE_STATEMENT, delete_regex(';'), [TEST_DELETE_STATEMENT]),
     (TEST_UPDATE_STATEMENT, update_regex(';'), [TEST_UPDATE_STATEMENT]),
     (TEST_CREATE_TABLE_COLUMNS_STATEMENT, create_table_regex(';'), [TEST_CREATE_TABLE_COLUMNS_STATEMENT]),
     (TEST_CREATE_TABLE_LIKE_STATEMENT, create_table_regex(';'), [TEST_CREATE_TABLE_LIKE_STATEMENT]),
     (TEST_CREATE_TABLE_QUERY_STATEMENT, create_table_regex(';'), [TEST_CREATE_TABLE_QUERY_STATEMENT]),
     (TEST_DROP_TABLE_STATEMENT, drop_table_regex(';'), [TEST_DROP_TABLE_STATEMENT]),
     (TEST_TRUNCATE_STATEMENT, truncate_regex(';'), [TEST_TRUNCATE_STATEMENT]),
     (TEST_PROCEDURE, procedure_regex(';;'), [TEST_PROCEDURE_EXPECTED])]
)
def test_regex(statement, regex_function, expected):

    result = re.findall(regex_function, statement)
    assert result == expected
