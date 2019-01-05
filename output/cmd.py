from colorama import Fore, Style
from config.config import ACCEPTED_DML_TYPES
from typing import List
from sql.objects import Procedure


def beautify(results: List[Procedure]) -> None:
    """
    Convenience function displaying the parsing results in a colored and human-readable format using
    colorama (as it works on all platforms)
    :param results: results list containing all procedures
    :return: None, only displays the results
    """

    msg = f'\n====> Parsing results <===='

    for p in results:
        msg += f'\n\n{Fore.GREEN}----------------------------\n'
        msg += f'{Fore.GREEN}{p.name} ({p.path})\n'
        msg += f'{Fore.GREEN}----------------------------\n{Style.RESET_ALL}'
        for q in p.queries:
            msg += f'|\n|--- {Fore.BLUE}{q.operation}{Style.RESET_ALL} ' \
                   f'----> {Fore.CYAN}{q.target_table.name}\n{Style.RESET_ALL}'

            if q.operation in ACCEPTED_DML_TYPES:
                if q.from_table:
                    for f in q.from_table:
                        msg += f'{Fore.CYAN}                  ' \
                               f'. {Fore.BLUE}FROM{Fore.CYAN} {f.name}{Style.RESET_ALL}\n'
                if q.join_table:
                    for f in q.join_table:
                        msg += f'{Fore.CYAN}                  ' \
                               f'. {Fore.BLUE}JOIN{Fore.CYAN} {f.name}{Style.RESET_ALL}\n'
            if q.target_columns:
                msg += f'. {Fore.BLUE}Columns --> {Fore.CYAN} {q.target_columns}{Style.RESET_ALL}\n\n'

    print(msg)
