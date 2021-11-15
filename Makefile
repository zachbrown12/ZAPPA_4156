.PHONY : test trade flake8 html_coverage
# Run all tests
test:
	make trade

# Run trade_simulation tests only
trade:
	python3.8 zappa/manage.py test trade_simulation.tests

# Run flake8 and generate output to bugs.txt
flake8:
	python3.8 -m flake8 > bugs.txt

# Run html_coverage command
html_coverage:
	python3 -m coverage html
