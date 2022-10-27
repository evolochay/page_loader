py := poetry run

package_dir := page_loader
tests_dir := tests
code_dir := $(package_dir) $(tests_dir)
reports_dir := reports


install:
	poetry install


build:
	poetry build


page-loader:
	$(py) page-loader


package-install:
	python3 -m pip install --user dist/*.whl


package-reinstall:
	python3 -m pip install --force-reinstall --user dist/*.whl


lint:
	$(py) flake8 page_loader


test-coverage:
	$(py) pytest --cov=page_loader --cov-report xml tests/

.PHONY: test-coverage
cool-coverage:  ## Make code-coverage html report
	mkdir -p $(reports_dir)/tests/
	$(py) pytest --cov=$(code_dir) --html=$(reports_dir)/tests/index.html $(tests_dir)/
	$(py) coverage html -d $(reports_dir)/coverage

.PHONY: test-coverage-view
coverage-view:  ## View code-coverage report in browser
	$(py) coverage html -d $(reports_dir)/coverage
	python3 -c "import webbrowser; webbrowser.open('file://$(shell pwd)/reports/coverage/index.html')"
