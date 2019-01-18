export PYTHONPATH=$PYTHONPATH:$(PWD)
export LAMBDA_TASK_ROOT=$(PWD)
export AWS_DEFAULT_REGION=eu-west-1
export TF=$(TERRAFORM)/.bin/terraform
export STAGE=dev

venv: venv/bin/activate

venv/bin/activate: requirements.txt
	test -d venv || python3 -m venv venv
	find ./** -type f -name requirements.txt -execdir $(PWD)/venv/bin/pip install -Ur requirements.txt \;
	touch venv/bin/activate

check: unit_test lint

lint: venv
	venv/bin/flake8 src tests

unit_test: venv
	venv/bin/py.test -vvvv -r sxX tests/unit

e2e_test: venv
	venv/bin/py.test -vvvv -r sxX tests/e2e

test: venv unit_test e2e_test
