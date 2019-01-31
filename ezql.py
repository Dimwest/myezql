import fire
from configparser import ConfigParser
from utils.validation import *
from utils.logging import *
from parse.worker import Worker
from output.cmd import beautify
from output.mermaid import Mermaid
from output.json import to_json
from typing import Optional, List


class MyEzQl(object):

    @with_logging
    def parse(self, i: str, ds: Optional[str]=None, dl: Optional[str]=None,
              mode: Optional[str]=None, chart: Optional[str]=None,
              json: Optional[str]=None, tables: Optional[List[str]]= None
              ) -> None:

        """
        Core function parsing input file or directory and pretty-printing results
        in the terminal.
        Provides various parsing and output options to tweak according to needs.

        :param i: path to input .sql file or directory containing .sql files

        :param ds: default schema, can be set in config.py for convenience purpose

        :param dl: delimiter, defaults to ;;

        :param mode: parsing mode, can be 'procedure' or 'ddl'

        :param chart: path to output .html flowchart, defaults to '', in which case
        no output file is created

        :param json: path to output .json file, defaults to '', in which case
        no output file is created

        :param tables: list of table names to focus on in the analysis, only the parents
        and children of these tables will be kept in the outputs
        """

        # Read config
        parser = ConfigParser()
        parser.read('config.ini')

        # Validate arguments
        validate_input_path(i)
        validate_output_path(chart, 'html')
        validate_output_path(json, 'json')
        tables = validate_tables(tables)

        # Set default schema to config value if not provided
        ds = parser['parser_config']['default_schema'] if not ds else ds

        # Set delimiter to config value if not provided
        dl = parser['parser_config']['delimiter'] if not dl else dl

        # Set parsing mode to config value if not provided
        mode = parser['parser_config']['default_mode'] if not mode else mode

        logger.info(f'\nStart parsing with parameters:'
                    f'\n  default schema --> {ds}'
                    f'\n  delimiter      --> {dl}'
                    f'\n  parsing mode   --> {mode}\n')

        # Configure and run parser
        worker = Worker(default_schema=ds, delimiter=dl, mode=mode)
        worker.run(i)

        # If filter defined, apply to results
        if tables:
            worker.simple_filter(tables)

        # Pretty print results
        beautify(worker.results)

        # If .html flowchart output required, create it
        if chart:
            m = Mermaid(worker.results)
            m.tables_chart(chart)
            logger.info(f'{chart} successfully saved')

        if json:
            to_json(worker.results, json)
            logger.info(f'{chart} successfully saved')


if __name__ == '__main__':

    fire.Fire(MyEzQl)
