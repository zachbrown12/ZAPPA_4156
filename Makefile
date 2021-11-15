html_coverage:
	python3 -m coverage html

test_trade_simulation:
	python3 zappa/manage.py test trade_simulation.tests

flake8:
	python3 -m flake8 > bugs.txt
