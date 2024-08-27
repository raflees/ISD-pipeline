gcloud functions deploy event_detector_test \
    --gen2 \
    --region=us-central1 \
    --runtime=python312 \
    --memory=256MB \
    --source=./event_detector \
    --entry-point=event_detector \
    --trigger-http --allow-unauthenticated