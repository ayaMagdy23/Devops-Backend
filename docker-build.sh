#!/bin/bash

# Build the Docker image
docker build -t myapp:latest .

# Optionally tag the image with a version
docker tag myapp:latest myapp:v1.0.0

# Push the image to a Docker registry (Docker Hub or private registry)
docker push myapp:latest
docker push myapp:v1.0.0
