import ujson
from typing import List, Dict


def to_json(results: List[Dict], path: str) -> None:

    """
    Transform and save results as .json file.

    :param results:
    :param path:
    :return:
    """

    output = {x['path']: [] for x in results}
    for x in results:
        output[x['path']].append(x)

    with open(path, 'w') as file:
        ujson.dump(output, file, indent=4)
