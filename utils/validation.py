import os
from utils.paths import is_path_creatable, is_pathname_valid


def validate_output_path(path, fmt):

    if path:
        if not (is_pathname_valid(path) and path.endswith(fmt)):
            raise OSError(f'{path} is not a valid .{fmt} file name')
        elif not (is_path_creatable(path) and path.endswith(fmt)):
            raise OSError(f'output {fmt} file cannot be created at {path}')


def validate_input_path(path):

    if not os.path.isdir(path) and not (os.path.isfile(path)
                                        and is_pathname_valid(path)
                                        and path.endswith('.sql')):
        raise OSError(f'{path} is not a valid directory or .sql file path')


def validate_tables(tables):

    zipper = ['schema', 'name']
    if tables:
        if any(not isinstance(t, str) or t.count('.') != 1 for t in tables):
            raise ValueError(f'All table values must be strings and have the '
                             f'following format: schema.name')
        else:
            tables = [dict(zip(zipper, t.split('.'))) for t in tables]
            return tables


def validate_parsing_mode(pmode):

    supported_modes = ('ddl', 'procedure')

    if pmode and pmode not in supported_modes:
        raise ValueError(f'Parsing mode must be one of the following values: '
                         f'{supported_modes}')


def validate_filter_mode(tables, fmode):

    supported_modes = ('simple', 'rec')

    if fmode:
        if not tables:
            raise ValueError(f'Filter mode can only be set if tables are specified')
        if fmode not in ('simple', 'rec'):
            raise ValueError(f'Filter mode must be one of the following values: '
                             f'{supported_modes}')
