install:
	poetry install


build:
	poetry build


page-loader:
	poetry run loader


package-install:
	python3 -m pip install --user dist/*.whl


package-reinstall:
	python3 -m pip install --force-reinstall --user dist/*.whl


make lint:
	poetry run flake8 main


make test-coverage:
	poetry run pytest --cov=main --cov-report xml tests/
