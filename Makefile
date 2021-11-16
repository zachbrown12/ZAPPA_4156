.PHONY : test trade flake8 html_coverage
# Run all tests and generate coverage
test:
	coverage run --source='.' zappa/manage.py test zappa
	coverage html

# Run trade_simulation tests only
trade:
	python3 zappa/manage.py test trade_simulation.tests

# Run api tests only
api:
	python3 zappa/manage.py test api.tests

# Run flake8 and generate output to bugs.txt
flake8:
	python3 -m flake8 --extend-exclude=./.venv,./zappa/.venv > bugs.txt

# Run html_coverage command
html_coverage:
	python3 -m coverage html
