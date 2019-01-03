import pytest
from antlrparser.extractor import FileProcessor, Mapper
from sql.objects import Procedure, Query, Table
from sqlparse import format as fmt
from config.config import DEFAULT_SCHEMA

procedure_path = './tests/resources/procedure.sql'
insert_path = './tests/resources/insert.sql'
update_path = './tests/resources/update.sql'
delete_path = './tests/resources/delete.sql'

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

INSERT_EXPECTED = Query(procedure='testproc',
                        operation='INSERT',
                        from_table=[Table(name='src_tab_1', schema=DEFAULT_SCHEMA)],
                        join_table=[Table(name='src_tab_2', schema=DEFAULT_SCHEMA),
                                    Table(name='src_tab_3', schema=DEFAULT_SCHEMA)],
                        target_table=Table(name='mytable', schema=DEFAULT_SCHEMA),
                        target_columns=['col_1', 'col_2', 'col_3', 'col_4', 'col_5', 'col_6', 'col_7'])

UPDATE_EXPECTED = Query(procedure='testproc',
                        operation='UPDATE',
                        join_table=[Table(name='src_tab_9', schema=DEFAULT_SCHEMA)],
                        target_table=Table(name='src_tab_8', schema=DEFAULT_SCHEMA),
                        target_columns=['tab_8.col_3=tab_9.col4', 'tab_8.col_4=tab_9.col5'])

DELETE_EXPECTED = Query(procedure='testproc',
                        operation='DELETE',
                        target_table=Table(name='src_tab_10', schema=DEFAULT_SCHEMA))

PROCEDURE_EXPECTED = Procedure(path=procedure_path,
                               name='testproc',
                               schema='example',
                               queries=[INSERT_EXPECTED, UPDATE_EXPECTED, DELETE_EXPECTED])


def test_parse_object_name():

    # Ensure that object name gets correctly split
    processor = FileProcessor()
    assert processor.parse_object_name('example.testproc') == ('example', 'testproc')


def test_get_procedure_name():

    # Ensure that procedure name gets correctly identified and split
    processor = FileProcessor()
    assert processor.get_procedure_name(TEST_PROCEDURE) == ('example', 'testproc')


def test_parse_procedure():

    # Run parser on test procedure file
    processor = FileProcessor()
    processor.parse_procedure(procedure_path, TEST_PROCEDURE)
    p = processor.results[0]

    # Check equality at Procedure level
    assert p.name == PROCEDURE_EXPECTED.name
    assert p.schema == PROCEDURE_EXPECTED.schema
    assert p.path == PROCEDURE_EXPECTED.path

    assert len(p.queries) == len(PROCEDURE_EXPECTED.queries)

    # Check equality and order at Query level
    for i, q in enumerate(p.queries):
        assert PROCEDURE_EXPECTED.queries[i].procedure == q.procedure
        assert PROCEDURE_EXPECTED.queries[i].operation == q.operation
        if q.target_columns or PROCEDURE_EXPECTED.queries[i].target_columns:
            assert PROCEDURE_EXPECTED.queries[i].target_columns == q.target_columns

        # Check equality at Table level
        assert PROCEDURE_EXPECTED.queries[i].target_table.__dict__ == q.target_table.__dict__

        if q.from_table or PROCEDURE_EXPECTED.queries[i].from_table:
            for j, t in enumerate(q.from_table):
                assert PROCEDURE_EXPECTED.queries[i].from_table[j].__dict__ == t.__dict__

        if q.join_table or PROCEDURE_EXPECTED.queries[i].join_table:
            for j, t in enumerate(q.join_table):
                assert PROCEDURE_EXPECTED.queries[i].join_table[j].__dict__ == t.__dict__


@pytest.mark.parametrize(
    "test_input, dmltype, expected",
    [(TEST_INSERT_STATEMENT, 'INSERT', INSERT_EXPECTED),
     (TEST_UPDATE_STATEMENT, 'UPDATE', UPDATE_EXPECTED),
     (TEST_DELETE_STATEMENT, 'DELETE', DELETE_EXPECTED)]
)
def test_parse_statement(test_input, dmltype, expected):

    processor = FileProcessor()
    mapper = Mapper()
    r = processor.parse_statement(dmltype=dmltype, s=test_input, mapper=mapper)

    # Check equality at Query level
    assert expected.operation == r.operation
    if expected.target_columns or r.target_columns:
        assert expected.target_columns == r.target_columns

    # Check equality at Table level
    assert expected.target_table.__dict__ == r.target_table.__dict__

    if r.from_table or expected.from_table:
        for j, t in enumerate(r.from_table):
            assert expected.from_table[j].__dict__ == t.__dict__

    if r.join_table or expected.join_table:
        for j, t in enumerate(r.join_table):
            assert expected.join_table[j].__dict__ == t.__dict__


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
