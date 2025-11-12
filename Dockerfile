# Dockerfile

FROM ghcr.io/astral-sh/uv:latest as uv

FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY --from=uv /uv /uvx /bin/

COPY pyproject.toml uv.lock ./

COPY . .

RUN uv sync --locked

CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]