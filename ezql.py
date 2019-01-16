import fire
from config import *
from utils.paths import *
from utils.logging import *
from parse.runner import Runner
from output.json import to_json
from output.cmd import beautify
from output.mermaid import Mermaid


class MyEzQl(object):

    @with_logging
    def parse(self, i: str, ds='', dl=';;', p: bool=True, json: str='', chart: str='') -> None:

        """
        Core function parsing input file or directory and pretty-printing results
        in the terminal.
        Provides various parsing and output options to tweak depending on the needs.

        :param i: path to input .sql file or directory containing .sql files

        :param ds: default schema, can be set in config.py for convenience purpose

        :param dl: delimiter, defaults to ;;

        :param p: procedure parsing mode, if True, looks for create procedure statements
        and parses all supported DDL statements inside of them, if False, simply looks
        for all support DDL statements in the file(s) parsed

        :param json: path to output .json file, defaults to '', in which case no .json
        is created

        :param chart: path to output .html flowchart, defaults to '', in which case
        no output file is created
        """

        # Validate input and output paths
        validate_input_path(i)
        validate_output_path(json, 'json')
        validate_output_path(chart, 'html')

        # Set default schema to config.py value if not given
        if not ds:
            ds = DEFAULT_SCHEMA

        # Set parsing type (there might be more options in the future)
        p = 'procedure' if p else 'ddl'

        # Create and run parser
        processor = Runner(default_schema=ds, delimiter=dl, mode=p)
        processor.run(i)

        # Pretty print results
        beautify(processor.results)

        # If .json output required, create it
        if json:
            to_json(processor.results, json)
            logger.info(f'-> {json} successfully saved')

        # If .html flowchart output required, create it
        if chart:
            m = Mermaid(processor.results)
            m.tables_chart(chart)
            logger.info(f'-> {chart} successfully saved')


if __name__ == '__main__':

    fire.Fire(MyEzQl)
