html_coverage:
	python3 -m coverage html

test:
	python3 -m coverage run -m unittest discover

flake8:
	python3 -m flake8 > bugs.txt