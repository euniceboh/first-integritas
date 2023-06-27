# RUN WITH TAG -j2
# npm 9.6.7
# node 18.12.1

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

# unit_test:
# 	. ./venv/Scripts/activate; \
# 	cd src; \
# 	cd tests; \
# 	pytest test_unit.py

# # need to fix webdriverexception bug here
# integration_test:
# 	. ./venv/Scripts/activate; \
# 	cd src; \
# 	cd tests; \
# 	pytest test_integration.py

clean:
	rm -rf venv; \
	cd src; rm -rf __pycache__; \
	cd tests; rm -rf __pycache__; \
	cd ..; cd node; rm -rf node_modules

.PHONY: run clean



