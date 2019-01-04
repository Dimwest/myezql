import fire
from utils.utils import *
from antlrparser.extractor import FileProcessor
from output.json import to_json
from output.cmd import beautify
import os


class MyEzQl(object):

    @staticmethod
    def show(i: str, o: str=None) -> None:
        """"""

        if o:
            if not (is_pathname_valid(o) and is_path_creatable(o) and o.endswith('.json')):
                print(f'Error: {o} is whether not valid, or cannot be created')
                return

        processor = FileProcessor()

        if os.path.isdir(i):
            processor.parse_dir(i)
        elif os.path.isfile(i) and is_pathname_valid(i) and i.endswith('.sql'):
            processor.parse_file(i)
        else:
            print(f'Error: {i} is not a valid path')
            return
        r = processor.results
        beautify(r)
        if o:
            to_json(r, o)
            print(f'-> {o} successfully saved')


if __name__ == '__main__':

    fire.Fire(MyEzQl)
