import ujson
import itertools
from sql.objects import Procedure
from typing import List


def to_json(results: List[Procedure], path: str) -> None:

    """
    Convenience function exporting parse results to a JSON file at the path specified as utils.

    :param results: list of results from parse.runner.Runner object
    :param path: target directory storing JSON file
    """

    to_dict = dict()
    for p in results:
        to_dict[p.name] = p.__dict__
        to_dict[p.name]['queries'] = [q.__dict__ for q in p.statements]

    with open(path, 'w') as fp:
        ujson.dump(to_dict, fp, indent=4, sort_keys=True)


def summarize(path: str) -> None:

    """
    Function analyzing JSON file generated and pretty-printing statistics about execution.

    :param path: directory in which the sql-wf.json file has been generated.
    """

    with open(path, 'r') as file:
        results = ujson.loads(file.read())

    has_dml = len([x for x in results.values() if x.get('queries')])
    queries = [x['queries'] for x in results.values()]
    queries = list(itertools.chain.from_iterable(queries))

    has_target = len([x for x in queries if x.get('target_table')])
    has_source = len([x for x in queries if x.get('from_table') or x.get('join_table')])
    has_columns = len([x for x in queries if x.get('target_columns')])
    n_dmls = {q['operation']: 0 for q in queries}
    for q in queries:
        n_dmls[q['operation']] += 1

    print(f"Reading results from: {path}")
    print(f"{len(results)} procedures found")
    print(f"    --> {has_dml} procedures containing DML statements")
    print(f"    --> {len(queries)} DML statements found")
    print(f"        - {has_target} with target table")
    print(f"        - {has_source} with source table(s)")
    print(f"        - {has_columns} with columns information")
    print(f"        - DML types:")
    for k in n_dmls.keys():
        print(f"            {n_dmls[k]} {k} statement(s)")
    print('\n')

    print('###################################################################################')
