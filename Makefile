krecik_tescik:
	mypy ./src
	ruff check ./src
	black ./src --diff --check
	pytest ./src

fix:
	ruff check ./src --fix
	black ./src
