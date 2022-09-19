# py := poetry run

# package_dir := page_loader
# tests_dir := tests
# code_dir := $(package_dir) $(tests_dir)
# reports_dir := reports


install:
	poetry install


build:
	poetry build


page-loader:
	poetry run page-loader


package-install:
	python3 -m pip install --user dist/*.whl


package-reinstall:
	python3 -m pip install --force-reinstall --user dist/*.whl


make lint:
	poetry run flake8 page_loader


 make test-coverage:
	poetry run pytest --cov=page_loader --cov-report xml tests/

# .PHONY: test-coverage
# test-coverage:  ## Make code-coverage report
#	mkdir -p $(reports_dir)/tests/
#	$(py) pytest --cov=$(code_dir) --html=$(reports_dir)/tests/index.html $(tests_dir)/
#	$(py) coverage html -d $(reports_dir)/coverage

# .PHONY: test-coverage-view
# test-coverage-view:  ## View code-coverage report in browser
#	$(py) coverage html -d $(reports_dir)/coverage
#	python3 -c "import webbrowser; webbrowser.open('file://$(shell pwd)/reports/coverage/index.html')"
