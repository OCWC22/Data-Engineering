#!/bin/bash
set -e

# --- Configuration ---
MINIO_ENDPOINT="http://localhost:9000"
AWS_ACCESS_KEY_ID="minioadmin"
AWS_SECRET_ACCESS_KEY="minioadmin"
BUCKET_NAME="neuralake-bucket"

# --- Helper Functions ---
function check_command() {
  if ! command -v $1 &> /dev/null; then
    echo "Error: $1 is not installed. Please install it to continue."
    exit 1
  fi
}

function wait_for_minio() {
  echo "Waiting for MinIO to be ready..."
  # A simple sleep is sufficient for local startup.
  # More advanced scripts might poll the health endpoint.
  sleep 5
}

# --- Main Script ---
echo "--- Checking Prerequisites ---"
check_command docker
check_command aws

echo -e "\\n--- Starting MinIO using Docker Compose ---"
# Navigate to the script's directory to ensure docker-compose.yml is found
cd "$(dirname "$0")"
docker-compose up -d

wait_for_minio

echo -e "\\n--- Configuring AWS CLI for MinIO ---"
# Set environment variables for the AWS CLI to use MinIO credentials
export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
AWS_ARGS="--endpoint-url $MINIO_ENDPOINT"

echo -e "\\n--- Checking if bucket '$BUCKET_NAME' exists ---"
if aws $AWS_ARGS s3api head-bucket --bucket "$BUCKET_NAME" 2>/dev/null; then
  echo "Bucket '$BUCKET_NAME' already exists. Skipping creation."
else
  echo "Bucket '$BUCKET_NAME' does not exist. Creating it..."
  aws $AWS_ARGS s3 mb "s3://$BUCKET_NAME"
  echo "Bucket '$BUCKET_NAME' created successfully."
fi

echo -e "\\n--- MinIO setup complete ---"
echo "You can access the MinIO console at http://localhost:9001"
echo "Access Key: $AWS_ACCESS_KEY_ID"
echo "Secret Key: $AWS_SECRET_ACCESS_KEY" 