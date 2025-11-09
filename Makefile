install:
	uv sync

migrate:
	python manage.py migrate

collectstatic:
	python manage.py collectstatic --noinput

lint:
	uv run ruff check

start:
	python manage.py runserver 0.0.0.0:8000

render-start:
	gunicorn task_manager.wsgi

build:
	./build.sh
