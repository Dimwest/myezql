# MyEzQL

MyEzQl is a Python CLI tool parsing MySQL-syntax files and enabling easier understanding and visualization of data flows 
described in those files.

## How to

Read from any SQL file or directory containing SQL files:

```bash
python3 ezql.py show --i /my/path.sql
python3 ezql.py show --i /my/dir
```

Here is a sample result:

![MyEzQL screenshot](README.png?raw=true "MyEzQL screenshot")

"Create procedure" statements can be parsed specifically by setting the --p flag to 1 or True.
If not set, DDL statements will be parsed without being tied to the eventual procedure containing them.
```bash
python3 ezql.py show --i /my/path.sql --p 1
```

Statement delimiter can be specified using the --dl flag.
If not specified as command line argument, the delimiter will have the value defined in config/config.py. By default, it's ';;'.
If the --p flag is set to True, this delimiter is used for procedures only, and it is assumed that individual DDL statements inside of the procedure use ';' as delimiter.
```bash
python3 ezql.py show --i /my/path.sql --dl ';;'
```

A default schema can be specified using the --ds flag.
If not specified as command line argument, the default schema will have the value defined in config/config.py
```bash
python3 ezql.py show --i /my/path.sql --ds default
```

Results can optionally be saved in a .json file 
```bash
python3 ezql.py show --i /my/path.sql --o /output/file.json
```

## To-do

#### Refactoring:
- [ ] Improve project structure
- [ ] Refactor output functions
- [ ] Look for potential redundancy functions in processor logic, move as much as possible to utils
- [x] Add type hints

#### Tests:
- [ ] Finish smaller units testing
- [ ] Add more cases
- [x] Add end-to-end testing of processing

#### Tool functionalities:
- [ ] Pass default schema via cmd
- [ ] Improve output
- [ ] New DDL statements
- [ ] Add proper config file
- [ ] Add install script
- [ ] Store JSONs in local TinyDB
- [x] Add "all DDL" and "all procedures" modes
- [x] Add multiprocessing at file parsing level
- [x] Introduce python-fire (https://github.com/google/python-fire)
- [x] Split FROM and JOIN tables
- [x] Add first draft

