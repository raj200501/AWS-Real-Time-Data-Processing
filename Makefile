PYTHON ?= python

setup:
	$(PYTHON) -m pip install -r requirements.txt

lint:
	./scripts/lint.sh

fmt:
	@if $(PYTHON) -m black --version >/dev/null 2>&1; then \
		$(PYTHON) -m black src tests; \
	else \
		echo "black not installed; skipping format"; \
	fi

test:
	$(PYTHON) -m pytest

verify:
	./scripts/verify.sh

run:
	$(PYTHON) -m rtap.cli demo --events 8
