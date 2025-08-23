test:
	pytest --cov-report term-missing *.py
type:
	mypy *.py