PYTHON = $(shell which python3)

clean:
	@rm -rf bin include lib pyvenv.cfg

venv:
	@echo "Initialising venv:"
	@$(PYTHON) -m venv .
	@bin/pip3 install -r requirements.txt
	@echo "You now need to activate the venv."

test:
	@echo "Running tests:"
	@$(PYTHON) -m unittest

run:
	@$(PYTHON) -m gbce

.PHONY: test run clean
