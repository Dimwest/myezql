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

#### Parsed statements
- [x] Drop table
- [x] Truncate table
- [x] Create procedure
- [x] Insert into
- [x] Replace into
- [x] Update set
- [x] Delete from
- [x] Create table like
- [x] Create table columns
- [x] Create table as


#### Refactoring:
- [ ] Replace unnecessary SQL objects by JSON object
- [ ] Refactor output functions
- [ ] Improve logging, introduce verbose arg
- [x] Improve project structure
- [x] Add type hints

#### Tests / build:
- [ ] Add Travis CI setup
- [ ] Finish unit and e2e testing, add coverage report
- [ ] Add more cases to all tests
- [ ] Run real life test at large scale, verify manually
- [x] Introduce end-to-end testing of processing
- [x] Add most important unit tests

#### Tool functionalities:
- [ ] Analysis features: table/function childs, parents, etc.
- [ ] Log execution summary (return results and run summary from logging decorator)
- [ ] Add install script
- [ ] Store JSONs in local TinyDB
- [x] Add proper config file
- [x] Add HTML flowchart creation using Mermaid
- [x] New DDL statements
- [x] Pass default schema via cmd
- [x] Add "all DDL" and "all procedures" modes
- [x] Add multiprocessing at file parsing level
- [x] Introduce python-fire (https://github.com/google/python-fire)
- [x] Split FROM and JOIN tables
- [x] Add first draft
