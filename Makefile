export PYTHONPATH=$PYTHONPATH:$(PWD)

venv: venv/bin/activate

venv/bin/activate: requirements.txt
	test -d venv || python3 -m venv venv
	find ./** -type f -name requirements.txt -execdir $(PWD)/venv/bin/pip install -Ur requirements.txt -Ur requirements-test.txt \;
	touch venv/bin/activate

output_test: venv
	venv/bin/py.test -vvvv -r sxX tests/unit/test_output.py

filter_test: venv
	venv/bin/py.test -vvvv -r sxX tests/unit/test_filter.py

unit_test: venv
	venv/bin/py.test -vvvv -r sxX tests/unit

e2e_test: venv
	venv/bin/py.test -vvvv -r sxX tests/e2e

test: venv unit_test e2e_test
