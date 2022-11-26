PYTHON = python3
PIP = $(PYTHON) -mpip
ECHO = echo

requirements-dev:
ifneq (,$(wildcard ./requirements-dev.txt))
	@$(PIP) install -r requirements-dev.txt
endif

lint:
	@$(PYTHON) -mflake8 .

test:
	@$(PYTHON) -c 'print("Comming soon...")'

run:
	@$(PYTHON) -mfangorn $(ARGS)
