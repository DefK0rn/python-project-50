install:
	uv sync

gendiff:
	uv run gendiff

build:
	uv build

package-install:
	uv tool install dist/hexlet_code-0.1.0-py3-none-any.whl

test:
	uv run pytest

lint:
	uv run ruff check gendiff

check: test lint

test-coverage:
	uv run pytest --cov=gendiff --cov-report xml

test-coverage-html:
	uv run pytest --cov=gendiff --cov-report=html

.PHONY: install gendiff