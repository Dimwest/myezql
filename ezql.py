import fire
from configparser import ConfigParser
from utils.processing import str_to_sql_dict
from utils.validation import *
from utils.logging import *
from parse.worker import Worker
from output.cmd import beautify
from output.mermaid import Mermaid
from output.json import to_json
from typing import Optional, List
from pathlib import Path


class MyEzQl(object):

    def parse(self, i: str, ds: Optional[str]=None, dl: Optional[str]=None,
              pmode: Optional[str]=None, chart: Optional[str]=None,
              json: Optional[str]=None, tables: Optional[List[str]]=None,
              procedures: Optional[List[str]]=None,
              fmode: Optional[str]=None, v: Optional[str]=None) -> None:

        """
        Core function parsing input file or directory and pretty-printing results
        in the terminal.
        Provides various parsing and output options to tweak according to needs.

        :param i: path to input .sql file or directory containing .sql files

        :param ds: default schema, can be set in config.py for convenience purpose

        :param dl: delimiter, defaults to ;;

        :param pmode: parsing mode, can be 'procedure' or 'ddl'

        :param chart: path to output .html flowchart, defaults to '', in which case
        no output file is created

        :param json: path to output .json file, defaults to '', in which case
        no output file is created

        :param tables: list of table names to filter on, only the parents
        and children of these table(s) will be kept in the outputs.
        Procedures filtering has precedence over tables filtering.

        :param procedures: list of procedure names to filter on, only the
        statements located inside the selected procedure(s) will be kept
        in outputs. Procedures filtering has precedence over tables filtering.

        :param fmode: filtering mode, can be 'simple' or 'rec'

        :param v: verbosity level, which will ultimately set the DEBUG output level.
        Must be one of ('v', 'vv', 'vvv', 'vvvv'), defaults to None, resulting in
        logging.INFO logger level
        """

        # Read config
        cfg = ConfigParser()
        cfg.read(f'{Path(__file__).parent}/config.ini')

        # Set default schema to config value if not provided
        ds = cfg['parser_config']['default_schema'] if not ds else ds

        # Set delimiter to config value if not provided
        dl = cfg['parser_config']['delimiter'] if not dl else dl

        # Set parsing mode to config value if not provided
        pmode = cfg['parser_config']['default_parsing_mode'] if not pmode else pmode
        fmode = cfg['parser_config']['default_filter_mode'] if not fmode else fmode
        v = cfg['parser_config']['default_verbosity'] if not v else v

        validate_args(i, chart, json, tables, procedures, pmode, fmode, v)

        set_verbosity(v)

        logger.warning(f'\nStart parsing with parameters:'
                       f'\n\n  default schema --> {ds}'
                       f'\n  delimiter      --> {dl}'
                       f'\n  parsing mode   --> {pmode}'
                       f"\n  filter mode    --> {fmode if tables or procedures else 'off'} "
                       f"\n{'    -> on procedure(s) ' + str(procedures) if procedures else ''}"
                       f"\n{'    -> on table(s) ' + str(tables) if tables else ''}")

        # Configure and run parser
        worker = Worker(default_schema=ds, delimiter=dl, pmode=pmode, fmode=fmode)
        worker.run(i)

        # If procedure filter defined, apply filtering to results
        if procedures:
            procedures = str_to_sql_dict(procedures)
            worker.procedures_filter(procedures)

        # If tables filter defined, apply filtering to results
        if tables:
            tables = str_to_sql_dict(tables)
            worker.tables_filter(tables)

        # Pretty print results in terminal
        beautify(worker.results)

        # Print errored files if existing
        worker.execution_warnings()

        # If .html flowchart output required, create it
        if chart:
            m = Mermaid(worker.results)
            m.tables_chart(chart)

        if json:
            to_json(worker.results, json)


if __name__ == '__main__':

    fire.Fire(MyEzQl)
