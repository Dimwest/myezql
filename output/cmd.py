from colorama import Fore, Style
from typing import List, Dict
import sys


def beautify(results: List[Dict]) -> None:

    """
    Convenience function displaying the parsing results in a colored and human-readable format using
    colorama (as it works on all platforms)
    :param results: results list containing all procedures
    :return: None, only displays the results
    """

    msg = f''

    for p in results:

        title_len = len(f"| {p['schema']}.{p['name']} ({p['path']} |") + 1
        msg += f'\n{Fore.GREEN}{"".join(["-" for x in range(title_len)])}\n'
        msg += f"{Fore.GREEN}| {p['schema']}.{p['name']} ({p['path']}) |\n"
        msg += f'{Fore.GREEN}{"".join(["-" for x in range(title_len)])}\n{Style.RESET_ALL}'
        for q in p['statements']:
            msg += f"|\n|--- {Fore.BLUE}{q['operation']}{Style.RESET_ALL} " \
                   f"----> {Fore.CYAN}{q['target_table']['schema']}.{q['target_table']['name']}\n{Style.RESET_ALL}"

            if q.get('from_table'):
                for f in q['from_table']:
                    msg += f'{Fore.CYAN}                  ' \
                           f". {Fore.BLUE}FROM{Fore.CYAN} {f['schema']}.{f['name']}{Style.RESET_ALL}\n"
            if q.get('join_table'):
                for j in q['join_table']:
                    msg += f'{Fore.CYAN}                  ' \
                           f". {Fore.BLUE}JOIN{Fore.CYAN} {j['schema']}.{j['name']}{Style.RESET_ALL}\n"

            if q.get('target_columns'):
                msg += f". {Fore.BLUE}Columns --> {Fore.CYAN} {q['target_columns']}{Style.RESET_ALL}\n\n"

    print(msg)
