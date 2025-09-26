test:
	pytest --cov-report term-missing tests/*.py
type:
	mypy --strict src/LinSysSolver/*.py tests
change:
	git log --pretty=format:"%h%x09%x09%as%x09%s"
