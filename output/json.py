import ujson
from typing import List, Dict, Optional
from colorama import Fore, Style
from utils.logging import logger

def to_json(results: List[Dict], path: Optional[str]) -> Optional[Dict]:

    """
    Transform and save results as .json file.

    :param results: results from Worker object
    :param path: path to save JSON file at

    :return: dictionary output for easier testing
    """

    try:

        output = {x['path']: [] for x in results}
        for x in results:
            output[x['path']].append(x)

        if path:
            with open(path, 'w') as file:
                ujson.dump(output, file, indent=4)

        print(f'{Fore.GREEN}{path} successfully saved{Style.RESET_ALL}')
        return output

    except Exception as e:
        logger.error(f'{Fore.RED}Could not save JSON file at {path}{Style.RESET_ALL}')

