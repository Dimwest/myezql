import re


def create_table_regex(delimiter):
    return re.compile(r'CREATE\s(?:TEMPORARY)?\s?TABLE\s(?:IF\sNOT\sEXISTS\s)?.*?{}'.format(delimiter), re.DOTALL | re.IGNORECASE)


def drop_table_regex(delimiter):
    return re.compile(r'DROP\s(?:TEMPORARY)?\s?TABLE\s(?:IF\sEXISTS\s)?.*?{}'.format(delimiter), re.DOTALL | re.IGNORECASE)


def procedure_regex(delimiter):
    return re.compile(r'CREATE\s+?PROCEDURE.*?{}'.format(delimiter), re.DOTALL | re.IGNORECASE)


def insert_regex(delimiter):
    return  re.compile(r'INSERT\s+?INTO\s.*?{}'.format(delimiter), re.DOTALL | re.IGNORECASE)


def replace_regex(delimiter):
    return re.compile(r'REPLACE\s+?INTO.*?{}'.format(delimiter), re.DOTALL | re.IGNORECASE)


def update_regex(delimiter):
    return re.compile(r'UPDATE\s+.*?(?:\sSET\s).*?{}'.format(delimiter), re.DOTALL | re.IGNORECASE)


def delete_regex(delimiter):
    return re.compile(r'DELETE\s+?FROM.*?{}'.format(delimiter), re.DOTALL | re.IGNORECASE)


def truncate_regex(delimiter):
    return re.compile(r'TRUNCATE\s+.*?{}'.format(delimiter), re.DOTALL | re.IGNORECASE)


NAME_REGEX = re.compile(
        r'(?<=CREATE\sPROCEDURE\s)(?:IF\sNOT\sEXISTS\s)?([A-Za-z0-9._-]+)',
        re.IGNORECASE)
