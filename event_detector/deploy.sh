gcloud auth list

gcloud functions deploy event_detector_test \
    --gen2 \
    --region=us-central1 \
    --runtime=python312 \
    --memory=256MB \
    --entry-point=event_detector \
    --trigger-http --allow-unauthenticated