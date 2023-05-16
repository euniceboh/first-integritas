.ONESHELL:

.DEFAULT_GOAL := run

PYTHON = ./venv/Scripts/python
PIP = ./venv/Scripts/pip

venv/Scripts/activate: requirements.txt
	python -m venv venv; \
	. ./venv/Scripts/activate; \
	$(PYTHON) -m pip install --upgrade pip; \
	$(PIP) install -r requirements.txt

venv: venv/Scripts/activate
	. ./venv/Scripts/activate

run: venv
	$(PYTHON) src/app.py

unit_test:
	. ./venv/Scripts/activate; \
	cd src; \
	cd tests; \
	pytest test_unit.py

# need to fix webdriverexception bug here
integration_test:
	. ./venv/Scripts/activate; \
	cd src; \
	cd tests; \
	pytest test_integration.py

clean:
	cd src; rm -rf __pycache__
	cd ..; rm -rf venv

.PHONY: run clean



