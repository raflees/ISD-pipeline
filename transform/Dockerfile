FROM python:3.12

RUN pip install poetry==1.8.3

COPY . isd_transform/
WORKDIR ./isd_transform/

RUN poetry install && poetry shell

ENTRYPOINT ["dbt", "run"]