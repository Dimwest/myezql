import re
from config.config import DELIMITER

PROCEDURE_REGEX = re.compile(f'CREATE\s+?PROCEDURE.*?{DELIMITER}',
                             re.DOTALL | re.IGNORECASE)

INSERT_REGEX = re.compile('INSERT\s+?INTO.*?;', re.DOTALL | re.IGNORECASE)

REPLACE_REGEX = re.compile('REPLACE\s+?INTO.*?;', re.DOTALL | re.IGNORECASE)

UPDATE_REGEX = re.compile('UPDATE\s+.*?;', re.DOTALL | re.IGNORECASE)

DELETE_REGEX = re.compile('DELETE\s+?FROM.*?;', re.DOTALL | re.IGNORECASE)

NAME_REGEX = re.compile(
        '(?<=CREATE\sPROCEDURE\s)(?:IF\s+(NOT\s+)?EXISTS\s+)?([a-zA-Z.]+)',
        re.IGNORECASE)