lint:
	mypy ./src
	ruff check ./src
	black ./src --diff --check

test:
	pytest ./src

fix:
	ruff check ./src --fix
	black ./src
