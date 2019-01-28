[![Build Status](https://travis-ci.com/Dimwest/MyEzQL.svg?branch=master)](https://travis-ci.com/Dimwest/MyEzQL)

# MyEzQL

MyEzQL is a Python CLI tool parsing SQL files and enabling easier visualization of data flows 
by pretty-printing parsing results and exporting them as HTML flowcharts.


## Tutorial

Read from any SQL file or directory containing SQL files.

```bash
python3 ezql.py parse --i /my/path.sql
python3 ezql.py parse --i /my/dir
```

Here is a sample terminal output:

![MyEzQL screenshot](img/cmd.png?raw=true "MyEzQL CLI creenshot")

You can choose to parse "Create Procedure" statements, or simply all DDL statements,
by setting the --mode flag. Note that DDL statements will only be linked to the procedure
they belong to when running in procedure mode. In DDL mode, they'll simply be linked to the
file they belong to.
```bash
python3 ezql.py parse --i /my/path.sql --mode procedure
python3 ezql.py parse --i /my/path.sql --mode ddl
```

Statement delimiter can be specified using the --dl flag.
If not specified as command line argument, the delimiter will have the value defined in config/config.py.
If the --p flag is set to True, this delimiter is used for finding Create Procedure statements only, and it is assumed that individual DDL statements inside of the procedure use ';' as delimiter.
```bash
python3 ezql.py parse --i /my/path.sql --dl ';;'
```

A default schema can be specified using the --ds flag.
If not specified as command line argument, the default schema will have the value defined in config/config.py
```bash
python3 ezql.py parse --i /my/path.sql --ds default
```

Results can be saved as flowcharts in HTML files and/or as JSON files
```bash
python3 ezql.py parse --i /my/path.sql --chart /output/file.html
python3 ezql.py parse --i /my/path.sql --json /output/file.json
```
Here is sample output file:

![MyEzQL screenshot](img/flowchart.png?raw=true "MyEzQL flowchart screenshot")

## Good to know

- Although MyEzQL works fine with most SQL statements, keep in mind that its parser 
has been generated using ANTLR4 and MySQL 5.6 grammar, hence it does NOT support some 
statements present in other SQL dialects, such as 'WITH' clauses for example.

- MyEzQL supports parsing of nested subqueries.

- SQL reserved keywords used as table or column aliases (e.g. 'events') can cause parsing bugs,
resulting in a failure to extract information from the concerned statement(s).

- The generation of flowcharts summarizing very complex, entangled table relationships might be
difficult to read through.

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
- [x] Refactor output functions
- [x] Replace unnecessary SQL objects by dictionaries
- [x] Improve project structure
- [x] Add type hints

#### Tests / build:
- [ ] Add coverage report
- [ ] Write tests for output functions
- [x] Add Travis CI setup
- [x] Finish unit and e2e testing of parsing features
- [x] Test all statements
- [x] Introduce end-to-end testing of processing
- [x] Add most important unit tests

#### Tool functionalities:
- [ ] Analysis features: table/function childs, parents, etc.
- [ ] Improve logging, introduce verbose arg
- [ ] Log execution summary
- [ ] Add install script
- [x] Add proper config file
- [x] Add HTML flowchart creation using Mermaid
- [x] New DDL statements
- [x] Pass default schema via cmd
- [x] Add "all DDL" and "all procedures" modes
- [x] Add multiprocessing at file parsing level
- [x] Introduce python-fire (https://github.com/google/python-fire)
- [x] Split FROM and JOIN tables
- [x] Add first draft
