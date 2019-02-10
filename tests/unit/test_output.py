from output.json import to_json
from output.mermaid import Mermaid
from bs4 import BeautifulSoup

parsing_results = [{
            "schema": "dwh",
            "name": "mytestprocedure",
            "path": "my/test/path.sql",
            "statements": [
                {
                    "operation": "INSERT",
                    "target_table": {
                        "schema": "default_schema",
                        "name": "test_table_1"
                    },
                    "from_table": [
                        {
                            "schema": "default_schema",
                            "name": "test_table_2"
                        },
                        {
                            "schema": "default_schema",
                            "name": "test_table_3"
                        }
                    ],
                    "join_table": [
                        {
                            "schema": "default_schema",
                            "name": "test_table_4"
                        },
                        {
                            "schema": "default_schema",
                            "name": "test_table_5"
                        }
                    ],
                    "target_columns": [
                        "col_1",
                        "col_2",
                        "col_3",
                        "col_4",
                        "col_5",
                        "col_6"
                    ],
                    "procedure": "mytestprocedure"
                }
            ]
        }]

json_output_expected = {"my/test/path.sql": parsing_results}

with open(f'./tests/_resources/output/mermaid.html', 'r') as template:
    mermaid_expected = BeautifulSoup(template.read(), features="html.parser")


def test_output_json():
    assert to_json(parsing_results, None) == json_output_expected


def test_output_mermaid():
    m = Mermaid(parsing_results)
    assert m.tables_chart(None).string == mermaid_expected.string
