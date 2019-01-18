from tests.utils import *


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

    # Test inequality check for procedures
    b.path = 'other_path'
    assert a != b

    # Test equality check for statements
    c = Statement(procedure='proc', operation='op', target_table=Table(name='tab1', schema='schema'),
                  target_columns=['col1', 'col2'], from_table=[Table(name='tab2', schema='schema')],
                  join_table=[Table(name='tab2', schema='schema')])

    d = Statement(procedure='proc', operation='op', target_table=Table(name='tab1', schema='schema'),
                  target_columns=['col1', 'col2'], from_table=[Table(name='tab2', schema='schema')],
                  join_table=[Table(name='tab2', schema='schema')])

    assert c == d
    c.procedure = 'other_proc'
    assert c != d

    # Test equality check for tables
    e = Table(name='tab1', schema='schema')
    f = Table(name='tab1', schema='schema')

    assert e == f
    e.name = 'other_tab'
    assert e != f
