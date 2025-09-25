test:
	pytest --cov-report term-missing *.py
type:
	mypy --strict *.py

change:
	git log --pretty=format:"%h%x09%x09%as%x09%s"
