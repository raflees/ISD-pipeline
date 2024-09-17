FROM python:3.12

RUN pip install poetry==1.8.3

ENV DBT_PROFILES_DIR=.
ENV GOOGLE_APPLICATION_CREDENTIALS=credentials.json

COPY . isd_transform/
WORKDIR isd_transform/

RUN poetry config virtualenvs.create false

RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
RUN apt-get update && apt-get install google-cloud-cli -y

RUN gcloud auth activate-service-account isd-pipeline-transform@cellular-retina-427804-i7.iam.gserviceaccount.com --key-file=credentials.json

RUN poetry install
