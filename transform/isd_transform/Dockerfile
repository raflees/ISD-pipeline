FROM python:3.12-alpine

ENV POETRY_VERSION=1.8.3
ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PATH="$POETRY_HOME/bin:$PATH"

RUN apk update && apk add curl
RUN curl -sSL https://install.python-poetry.org | python3 -

ENV DBT_PROFILES_DIR=.

WORKDIR app/
COPY . .

# RUN poetry install --no-interaction --no-ansi --no-root
# ENTRYPOINT ["dbt", "run"]