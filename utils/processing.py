from typing import List, Dict


def str_to_sql_dict(tables: List[str]) -> List[Dict]:

    """
    Transforms a list of tables/procedures names into a list of dictionaries with keys schema and name

    :param tables: list ot table names
    :return: list of table dictionaries
    """

    return [dict(zip(['schema', 'name'], t.lower().split('.'))) for t in tables]


def flatten(l: List[List[Dict]]) -> List[Dict]:

    """
    Flattens list of lists.

    :param l: list containing lists of table dictionaries
    :return: list containing table dictionaries
    """
    return[item for sublist in l for item in sublist]


def merge_results(results: List[Dict]) -> List[Dict]:

    """
    Merges procedure/file dicts corresponding to the same procedure/file
    after recursive filtering.

    :param results: list of procedure/file dictionaries to merge
    :return: list of merged procedure/file dictionaries
    """

    combos = []

    # Create list of unique procedure/file dictionaries
    for x in results:
        c = {
            'name': x['name'],
            'path': x['path'],
            'schema': x['schema'],
            'statements': []
        }
        if c not in combos:
            combos.append(c)

    # Add all statements from results dictionaries to unique list's
    # statement attribute
    for x in combos:
        for y in results:
            if x['name'] == y['name'] \
                    and x['path'] == y['path'] \
                    and x['schema'] == y['schema']:
                x['statements'].extend(y['statements'])

    return combos
