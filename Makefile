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

run: venv test
	$(PYTHON) src/app.py

test:
	. ./venv/Scripts/activate; pytest

clean:
	cd src; rm -rf __pycache__
	cd ..; rm -rf venv

.PHONY: run clean



