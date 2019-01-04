import fire
from utils.utils import *
from antlrparser.extractor import FileProcessor
from output.json import to_json
from output.cmd import beautify
import os


class MyEzQl(object):

    def file(self, i, o=None):

        """"""

        if not (os.path.isfile(i) and is_pathname_valid(i)):
            print(f'Error: {i} is not a valid file path')
            return
        if o:
            if not (is_pathname_valid(o) and is_path_creatable(o)):
                print(f'Error: {o} is not a valid file path or cannot be created')
                return
            if not o.endswith('.json'):
                print(f'Error: {o} is not a valid JSON path')
                return

        processor = FileProcessor()
        processor.parse_file(i)
        r = processor.results
        beautify(r)
        if o:
            to_json(r, o)
            print(f'-> {o} successfully saved')

    def dir(self, i, o=None):
        """"""

        if not os.path.isdir(i):
            print(f'Error: {i} is not a valid directory')
            return
        if o:
            if not (is_pathname_valid(o) and is_path_creatable(o)):
                print(f'Error: {o} is not a valid file path or cannot be created')
                return
            if not o.endswith('.json'):
                print(f'Error: {o} is not a valid JSON path')
                return

        processor = FileProcessor()
        processor.parse_dir(i)
        r = processor.results
        beautify(r)
        if o:
            to_json(r, o)
            print(f'-> {o} successfully saved')


if __name__ == '__main__':

    fire.Fire(MyEzQl)
