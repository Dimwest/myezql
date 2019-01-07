import fire
from utils.paths import *
from utils.logging import *
from antlrparser.runner import Runner
from output.json import to_json
from output.cmd import beautify
from config import *
import os


class MyEzQl(object):

    @with_logging
    def show(self, i: str, o: str='', ds='', dl=';;', p: bool=False) -> None:

        if o:
            if not (is_pathname_valid(o) and is_path_creatable(o) and o.endswith('.json')):
                logger.error(f'Error: {o} is whether not valid, or cannot be created')
                return

        if not ds:
            ds = DEFAULT_SCHEMA

        p = 'procedure' if p else 'ddl'

        processor = Runner(default_schema=ds, delimiter=dl, mode=p)

        if os.path.isdir(i):
            processor.parse_dir(i)
        elif os.path.isfile(i) and is_pathname_valid(i) and i.endswith('.sql'):
            processor.results = processor.parse_file(i)
        else:
            logger.error(f'Error: {i} is not a valid path')
            return
        beautify(processor.results)
        if o:
            to_json(processor.results, o)
            logger.info(f'-> {o} successfully saved')


if __name__ == '__main__':

    fire.Fire(MyEzQl)
