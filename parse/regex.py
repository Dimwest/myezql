import re


def procedure_regex(delimiter):
    return re.compile(r'CREATE\s+?PROCEDURE.*?{}'.format(delimiter), re.DOTALL | re.IGNORECASE)


def insert_regex(delimiter):
    return  re.compile(r'INSERT\s+?INTO.*?{}'.format(delimiter), re.DOTALL | re.IGNORECASE)


def replace_regex(delimiter):
    return re.compile(r'REPLACE\s+?INTO.*?{}'.format(delimiter), re.DOTALL | re.IGNORECASE)


def update_regex(delimiter):

    # TODO -> Add SET to fix it and get rid of wrong matches
    return re.compile(r'UPDATE\s+.*?{}'.format(delimiter), re.DOTALL | re.IGNORECASE)


def delete_regex(delimiter):
    return re.compile(r'DELETE\s+?FROM.*?{}'.format(delimiter), re.DOTALL | re.IGNORECASE)


NAME_REGEX = re.compile(
        r'(?<=CREATE\sPROCEDURE\s)(?:IF\s+(NOT\s+)?EXISTS\s+)?([A-Za-z0-9._-]+)',
        re.IGNORECASE)
