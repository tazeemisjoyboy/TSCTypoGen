PYTHON ?= python3

.PHONY: install run test demo

install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt

run:
	FLASK_APP=app FLASK_ENV=development flask run --debug

test:
	pytest

demo:
	$(PYTHON) scripts/offline_demo.py
