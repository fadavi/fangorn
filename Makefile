PYTHON = python3
PIP = $(PYTHON) -mpip
ECHO = echo

requirements-dev:
ifneq (,$(wildcard ./requirements-dev.txt))
	@$(PIP) install -r requirements-dev.txt
endif

format:
	@$(PYTHON) -mautopep8 -air .

lint:
	@$(PYTHON) -mflake8 --count --select=E,F,W --show-source --statistics .

test:
	@$(PYTHON) -mpytest

run:
	@$(PYTHON) -mfangorn $(ARGS)
