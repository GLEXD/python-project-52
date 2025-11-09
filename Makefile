install:
	uv sync

migrate:
	python manage.py migrate

build:
	./build.sh

collectstatic:
	python manage.py collectstatic --noinput

start:
	python manage.py runserver 0.0.0.0:8000

render-start:
	gunicorn task_manager.wsgi

lint:
	uv run ruff check

test:
	uv run pytest --ds=task_manager.settings --reuse-db

coverage:
	uv run coverage run --omit='*/migrations/*,*/settings.py,*/venv/*,*/.venv/*' -m pytest --ds=task_manager.settings
	uv run coverage report --show-missing --skip-covered

ci-install:
	uv sync --group dev

ci-migrate:
	uv run python manage.py makemigrations --noinput && \
	uv run python manage.py migrate --noinput

ci-test:
	uv run coverage run --omit='*/migrations/*,*/settings.py,*/venv/*,*/.venv/*' -m pytest --ds=task_manager.settings --reuse-db
	uv run coverage xml
	uv run coverage report --show-missing --skip-covered