FROM python:3.12

RUN pip install poetry==1.8.3

ENV DBT_PROFILES_DIR=.

COPY . isd_transform/
WORKDIR isd_transform/

RUN poetry config virtualenvs.create false

RUN poetry install
ENTRYPOINT ["dbt", "run"]