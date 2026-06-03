PYTHON := $(if $(wildcard .venv/bin/python),.venv/bin/python,python)

.PHONY: test

test:
	$(PYTHON) -m unittest discover -s tests -p 'test_*.py'