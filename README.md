[![Build Status](https://travis-ci.com/Dimwest/MyEzQL.svg?branch=master)](https://travis-ci.com/Dimwest/MyEzQL)

# MyEzQL

MyEzQL is a Python CLI tool parsing SQL files and enabling easier visualization of data flows 
by pretty-printing parsing results and exporting them as HTML flowcharts.


## Tutorial

### Install

MyEzQL is currently not packaged yet (hopefully soon !), hence cannot be installed with pip.
It can easily be used with the following commands.

```bash
cd my/target/directory
git clone git@github.com:Dimwest/MyEzQL.git
cd MyEzQL/
make venv
source venv/bin/activate
```

Tip: As the only command used by the script is "parse", and the only required argument is the input path --i, you can set the following alias:

```bash
alias myezql="source /path/to/MyEzQL/venv/bin/activate && python3 /path/to/MyEzQL/ezql.py parse --i"
```

Don't forget to deactivate the virtual environment when you're done ;)

### Basic settings

Read from any SQL file or directory containing SQL files.

```bash
python3 ezql.py parse --i /my/path.sql
python3 ezql.py parse --i /my/dir
```

Here is a sample terminal output:

![MyEzQL screenshot](img/cmd.png?raw=true "MyEzQL CLI creenshot")

You can choose to parse "Create Procedure" statements, or simply all DDL statements,
by setting the --pmode (parsing mode) flag. Note that DDL statements will only be linked to the procedure
they belong to when running in procedure mode. In DDL mode, they'll simply be linked to the
file they belong to.
```bash
python3 ezql.py parse --i /my/path.sql --pmode procedure
python3 ezql.py parse --i /my/path.sql --pmode ddl
```

Statement delimiter can be specified using the --dl flag.
If not specified as command line argument, the delimiter will have the value defined in config.ini.
If the --pmode flag is set to True, this delimiter is used for finding Create Procedure statements only, 
and it is assumed that individual DDL statements inside of the procedure use ';' as delimiter.
```bash
python3 ezql.py parse --i /my/path.sql --dl ';;'
```

A default schema can be specified using the --ds flag.
If not specified as command line argument, the default schema will have the value defined in config.ini
```bash
python3 ezql.py parse --i /my/path.sql --ds default
```
Verbosity level can be adjusted using the --v flag.
If not specified as command line argument, the default schema will have the value defined in config.ini
will have the value defined in config.ini. Accepted values are: v, vv, vvv, vvvv

```bash
python3 ezql.py parse --i /my/path.sql --v vv
```


#### Save results as HTML flowcharts or JSON files

Results can be saved as flowcharts in HTML files and/or as JSON files
```bash
python3 ezql.py parse --i /my/path.sql --chart /output/file.html
python3 ezql.py parse --i /my/path.sql --json /output/file.json
```
Here is sample output HTML file:

![MyEzQL screenshot](img/flowchart.png?raw=true "MyEzQL flowchart screenshot")

#### Results filtering

Parsing of large amount of SQL code can result in large, entangled flowcharts which
results can be difficult to interpret. You may also want to focus your analysis
on one (or several) tables/procedures.

##### Tables filter

Results can be filtered on a list of specific tables using the --tables flag.
All tables in the list must specify a schema name.
```bash
python3 ezql.py parse --i /my/path.sql --tables "['schema.tab_name']"
```
NB: depending on the shell you're using, you might need to escape the argument list differently, or not at all.
This example works with zsh.

Tables filtering mode can be set using the --fmode flag. As of now, two modes are supported.

- Simple filtering will keep only the statements containing direct parents and children of the selected table(s)

```bash
python3 ezql.py parse --i /my/path.sql --tables "['schema.tab_name']" --fmode simple
```

- Recursive filtering will recursively get all statements containing direct and indirect parents and children of the selected table(s)

```bash
python3 ezql.py parse --i /my/path.sql --tables "['schema.tab_name']" --fmode rec
```

##### Procedures filter

Results can be filtered on a list of specific procedures using the --procedures flag.
All procedures in the list must specify a schema name. 

```bash
python3 ezql.py parse --i /my/path.sql --procedures "['schema.proc_name']"
```

Procedures filtering only has "simple" mode, hence the --fmode flag will not apply to this filter.

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


#### Refactoring / documenting:
- [x] Add install documentation
- [x] Refactor output functions
- [x] Replace unnecessary SQL objects by dictionaries
- [x] Improve project structure
- [x] Add type hints

#### Tests / build:
- [ ] Write tests proving unsupported cases (e.g. SQL keywords in aliases, etc.)
- [ ] Add test coverage report
- [x] Write tests for filter functions
- [x] Test on larger scale with 90 available procedure files
- [x] Write tests for output functions
- [x] Add Travis CI setup
- [x] Improve unit and e2e testing of parsing features
- [x] Test all statements
- [x] Introduce end-to-end testing of processing
- [x] Add unit tests

#### Tool features:
- [ ] Add aliases support
- [ ] Add column inheritance analysis (requires aliases support)
- [x] Improve logging, introduce verbosity arg
- [x] Add procedures' filtering
- [x] Analysis features: table/function childs, parents, etc.
- [x] Improve arguments validation
- [x] Add proper config file
- [x] Add HTML flowchart creation using Mermaid
- [x] New DDL statements
- [x] Pass default schema via cmd
- [x] Add "all DDL" and "all procedures" modes
- [x] Add multiprocessing at file parsing level
- [x] Introduce python-fire (https://github.com/google/python-fire)
- [x] Split FROM and JOIN tables
- [x] Add first draft
