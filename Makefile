install:
	poetry install


build:
	poetry build


main:
	poetry run main


package-install:
	python3 -m pip install --user dist/*.whl


package-reinstall:
	python3 -m pip install --force-reinstall --user dist/*.whl


make lint:
	poetry run flake8 main
