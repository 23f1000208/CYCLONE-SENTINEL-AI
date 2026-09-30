#!/usr/bin/env bash
set -e

echo "=========================================================="
echo "    CYCLONE SENTINEL AI - GOOGLE CLOUD RUN DEPLOYMENT     "
echo "=========================================================="

REGION=${1:-"asia-south1"}

echo "Verifying active GCP project..."
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)

if [ -z "$PROJECT_ID" ]; then
  echo "Error: No active GCP project set. Run: gcloud config set project YOUR_PROJECT_ID"
  exit 1
fi

echo "Deploying to GCP Project: $PROJECT_ID (Region: $REGION)"

# 1. Enable required APIs
echo "Enabling Cloud Run, Cloud Build, and Container Registry APIs..."
gcloud services enable run.googleapis.com cloudbuild.googleapis.com containerregistry.googleapis.com

# 2. Deploy Backend
echo "Building & Deploying FastAPI Backend..."
gcloud run deploy cyclone-backend \
  --source ./backend \
  --region "$REGION" \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars ENVIRONMENT=production,PORT=8080

BACKEND_URL=$(gcloud run services describe cyclone-backend --platform managed --region "$REGION" --format 'value(status.url)')
echo "Backend live at: $BACKEND_URL"

# 3. Deploy Frontend
echo "Building & Deploying Next.js Command Center..."
gcloud run deploy cyclone-frontend \
  --source ./frontend \
  --region "$REGION" \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars BACKEND_URL="$BACKEND_URL",NODE_ENV=production,PORT=8080

FRONTEND_URL=$(gcloud run services describe cyclone-frontend --platform managed --region "$REGION" --format 'value(status.url)')

echo "=========================================================="
echo "DEPLOYMENT COMPLETE!"
echo "Command Center: $FRONTEND_URL"
echo "Backend API:    $BACKEND_URL/docs"
echo "=========================================================="
