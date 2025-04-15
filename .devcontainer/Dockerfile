ARG POETRY_VERSION=2.1

FROM mcr.microsoft.com/devcontainers/python:3.12

ARG POETRY_VERSION

# * Install poetry in order to manage the dependencies
RUN pip install --upgrade pip && \
    pip install poetry==${POETRY_VERSION} && \
    poetry config virtualenvs.options.always-copy true && \
    poetry config virtualenvs.prompt "venv" && \
    poetry config virtualenvs.in-project true
