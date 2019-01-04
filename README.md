# MyEzQL

MyEzQl is a Python CLI tool parsing MySQL procedures and enabling easier understanding and visualization of data flows 
described in SQL files.

## How to use it

The tool is simple to use:
```bash
python3 ezql.py file --i /my/path.sql
python3 ezql.py dir --i /my/path/
```
Results can optionally be saved in .json files 
```bash
python3 ezql.py file --i /my/path.sql --0 /output/file.json
python3 ezql.py dir --i /my/path/ --0 /output/file.json
```

## To-do list

#### Refactoring:
- [ ] Improve project structure
- [ ] Refactor output functions
- [ ] Look for potential redundancy functions in processor logic, move as much as possible to utils
- [x] Add type hints

#### Tests:
- [ ] Finish smaller units testing
- [x] Add end-to-end testing of processing

#### Tool functionalities:
- [ ] Pass default schema via cmd
- [ ] New DDL statements
- [ ] Add multithreading at file level
- [ ] Add proper config file
- [ ] Add install script
- [ ] Store JSONs in local TinyDB
- [x] Introduce python-fire (https://github.com/google/python-fire)
- [x] Split FROM and JOIN tables
- [x] Add first draft

