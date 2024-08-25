#!/bin/bash

backend_image="puzzlecoder-backend"
backend_dockerfile="."

worker_image="puzzlecoder-worker"
worker_dockerfile=".\worker"

scaler_image="puzzlecoder-scaler"
scaler_dockerfile=".\scaler"


echo "Building Docker image: $backend_image"
docker build "$backend_dockerfile" -t "$backend_image"

echo "Building Docker image: $worker_image"
docker build "$worker_dockerfile" -t "$worker_image"

echo "Building Docker image: $scaler_image"
docker build "$scaler_dockerfile" -t "$scaler_image"

echo "All Docker images have been built successfully."