import fire
from configparser import ConfigParser
from utils.paths import *
from utils.logging import *
from parse.runner import Runner
from output.json import to_json
from output.cmd import beautify
from output.mermaid import Mermaid


class MyEzQl(object):

    @with_logging
    def parse(self, i: str, ds='', dl='', mode: str='', json: str='', chart: str='') -> None:

        """
        Core function parsing input file or directory and pretty-printing results
        in the terminal.
        Provides various parsing and output options to tweak according to needs.

        :param i: path to input .sql file or directory containing .sql files

        :param ds: default schema, can be set in config.py for convenience purpose

        :param dl: delimiter, defaults to ;;

        :param mode: parsing mode, can be 'procedure', 'ddl', or 'select'

        :param p: procedure parsing mode, if True, looks for create procedure statements
        and parses all supported DDL statements inside of them, if False, simply looks
        for all support DDL statements in the file(s) parsed

        :param json: path to output .json file, defaults to '', in which case no .json
        is created

        :param chart: path to output .html flowchart, defaults to '', in which case
        no output file is created
        """

        # Read config
        parser = ConfigParser()
        parser.read('config.ini')

        # Validate input and output paths
        validate_input_path(i)
        validate_output_path(json, 'json')
        validate_output_path(chart, 'html')

        # Set default schema to config value if not provided
        ds = parser['parser_config']['default_schema'] if not ds else ds

        # Set delimiter to config value if not provided
        dl = parser['parser_config']['delimiter'] if not dl else dl

        # Set parsing mode to config value if not provided
        mode = parser['parser_config']['default_mode'] if not mode else mode

        # Create and run parser
        logger.info(f'\nStart parsing with parameters:'
                    f'\n  default schema --> {ds}'
                    f'\n  delimiter      --> {dl}'
                    f'\n  parsing mode   --> {mode}\n')
        runner = Runner(default_schema=ds, delimiter=dl, mode=mode)
        runner.run(i)

        # Pretty print results
        beautify(runner.results)

        # If .json output required, create it
        if json:
            to_json(runner.results, json)
            logger.info(f'-> {json} successfully saved')

        # If .html flowchart output required, create it
        if chart:
            m = Mermaid(runner.results)
            m.tables_chart(chart)
            logger.info(f'-> {chart} successfully saved')


if __name__ == '__main__':

    fire.Fire(MyEzQl)
