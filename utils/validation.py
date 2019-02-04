import os
from typing import List, Dict, Optional
from utils.paths import is_path_creatable, is_pathname_valid


def validate_args(i: str, chart: str, json: str, tables: Optional[List[str]],
                  pmode: Optional[str], fmode: Optional[str]) -> None:

    """
    Validate all CLI arguments before execution, raise clear exceptions if
    validation does not succeed.

    :param i: input file/directory path
    :param chart: output html flowchart path
    :param json: output json file path
    :param tables: list of table names, defaults to None
    :param pmode: parsing mode, defaults to None
    :param fmode: filter mode, defaults to None
    """

    validate_input_path(i)
    validate_output_path(chart, 'html')
    validate_output_path(json, 'json')
    validate_tables(tables)
    validate_parsing_mode(pmode)
    validate_filter_mode(tables, fmode)


def validate_output_path(path: str, fmt: str) -> None:

    """
    Validate output file path argument for different formats, raises
    a ValueError if the file name is not valid or if the file cannot be
    created at the specified path.

    :param path: output path argument specified by the user
    :param fmt: file format, can be either json or html
    """

    if path:
        if not (is_pathname_valid(path) and path.endswith(fmt)):
            raise ValueError(f'{path} is not a valid .{fmt} file name')
        elif not (is_path_creatable(path) and path.endswith(fmt)):
            raise ValueError(f'output {fmt} file cannot be created at {path}')


def validate_input_path(path: str) -> None:

    """
    Validate input file/directory path argument, raises a ValueError if the path
    is not valid .sql file or directory.

    :param path: input path argument specified by the user
    """

    if not os.path.isdir(path) and not (os.path.isfile(path)
                                        and is_pathname_valid(path)
                                        and path.endswith('.sql')):
        raise ValueError(f'{path} is not a valid directory or .sql file path')


def validate_tables(tables: Optional[List[str]]) -> None:

    """
    Ensure list of tables has the format 'schema.name' and return a list
    of dictionaries with the format '{schema: schema, name: name}'
    :param tables: list of table names specified by the user
    :return: list of table dictionaries in the format used by the worker
    """

    if tables:
        if not isinstance(tables, list):
            raise ValueError(f'{tables} must be a list of strings')
        if any(not isinstance(t, str) or t.count('.') != 1 for t in tables):
            raise ValueError(f'All table values must be strings and have the '
                             f'following format: schema.name')


def validate_parsing_mode(pmode: Optional[str]) -> None:

    """
    Ensures parsing mode argument has one of the accepted values

    :param pmode: parsing mode argument, can be ddl or procedure
    """

    supported_modes = ('ddl', 'procedure')

    if pmode and pmode not in supported_modes:
        raise ValueError(f'Parsing mode must be one of the following values: '
                         f'{supported_modes}')


def validate_filter_mode(tables: Optional[List[Dict]], fmode: Optional[str]) -> None:

    """
    Ensures filter mode argument has one of the accepted values, and is only
    set if tables argument is set

    :param tables: list of table dictionaries, None if not set by user
    :param fmode: filter mode argument, can be simple or rec (recursive)
    """

    supported_modes = ('simple', 'rec')

    if fmode:
        if not tables:
            raise ValueError(f'Filter mode can only be set if tables are specified')
        if fmode not in ('simple', 'rec'):
            raise ValueError(f'Filter mode must be one of the following values: '
                             f'{supported_modes}')
