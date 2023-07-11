# RUN BOTH SERVERS WITH TAG -j2

.ONESHELL:

.DEFAULT_GOAL := run

PYTHON = ./venv/Scripts/python
PIP = ./venv/Scripts/pip

venv/Scripts/activate: src/requirements.txt
	python -m venv venv; \
	. ./venv/Scripts/activate; \
	$(PYTHON) -m pip install --upgrade pip; \
	$(PIP) install -r src/requirements.txt; \

venv: venv/Scripts/activate
	. ./venv/Scripts/activate

node:
	cd src; \
	cd node; \
	npm install; \
	node validator.js

flask: venv
	$(PYTHON) src/app.py

run: node flask

clean:
	rm -rf venv; \
	cd src; rm -rf __pycache__; \
	cd e2e_test; rm -rf __pycache__; \
	cd ..; cd node; rm -rf node_modules; \
	cd unit_test; rm -rf coverage

.PHONY: run clean



