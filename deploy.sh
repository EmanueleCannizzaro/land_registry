#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Configuration ---
PROJECT_ID="your-gcp-project-id" # TODO: Replace with your GCP Project ID
SERVICE_NAME="land-registry-app"
REGION="europe-west1" # TODO: Choose a region close to your users, e.g., europe-west1

# --- Build and Deploy ---

echo "Authenticating Docker to Google Container Registry..."
gcloud auth configure-docker

echo "Building Docker image..."
# The image name format is gcr.io/PROJECT_ID/SERVICE_NAME:TAG
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}:latest"
docker build -t "${IMAGE_NAME}" .

echo "Pushing Docker image to Google Container Registry..."
docker push "${IMAGE_NAME}"

echo "Deploying service to Google Cloud Run..."
gcloud run deploy "${SERVICE_NAME}" \
  --image "${IMAGE_NAME}" \
  --platform managed \
  --region "${REGION}" \
  --allow-unauthenticated \
  --project "${PROJECT_ID}" \
  --port 8080 \
  --set-env-vars "PORT=8080" \
  --memory 512Mi \
  --cpu 1 \
  --max-instances 1 \
  --min-instances 0 \
  --timeout 300 \
  --no-traffic # Deploy without immediately routing traffic to the new revision

echo "Deployment initiated. Check the Cloud Run console for status: https://console.cloud.google.com/run/detail/${REGION}/${SERVICE_NAME}/revisions?project=${PROJECT_ID}"
echo "Remember to replace 'your-gcp-project-id' with your actual GCP Project ID in this script."
echo "You might also want to adjust the region and other settings as needed."
