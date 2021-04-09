# global python binary
PYTHON_BIN = $(shell which python3)

# virtual env directories and binaries
VENV_DIR        = venv
VENV_PYTHON_BIN = $(VENV_DIR)/bin/python
PIP_BIN         = $(VENV_DIR)/bin/pip
BLACK_BIN       = $(VENV_DIR)/bin/black
TWINE_BIN       = $(VENV_DIR)/bin/twine

.PHONY: lint test build docs deploy

# setup dev environment, eg. `make venv`
$(VENV_DIR): requirements.txt requirements.dev.txt
	test -d $(VENV_DIR) || $(PYTHON_BIN) -m venv $(VENV_DIR) && $(PIP_BIN) install -U pip setuptools wheel
	$(PIP_BIN) install -r requirements.txt
	$(PIP_BIN) install -r requirements.dev.txt
	touch $(VENV_DIR)

lint:
	$(BLACK_BIN) .

test: ally/tests.py
	$(VENV_PYTHON_BIN) ally/tests.py

build:
	$(VENV_PYTHON_BIN) setup.py sdist bdist_wheel

docs:
	rm -rf docs
	mkdir docs
	cd sphinx && make clean && make html
	cp -a sphinx/_build/html/ docs
	touch docs/.nojekyll

deploy:
	$(TWINE_BIN) upload dist/*
