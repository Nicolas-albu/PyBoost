
test-env:
	@pytest -v tests/units/test_environment.py

test-builder:
	@pytest -v tests/units/test_builder.py

lint:
	@black --check .
	@isort --check .