#!/bin/bash

# Set environment variables (make sure these are set in your environment)
export DJANGO_SECRET_KEY="your-secret-key"
export DJANGO_DEBUG=False
export DATABASE_URL="your-database-url"
export ALLOWED_HOSTS="your-ec2-public-ip-or-domain"

# SSH into your EC2 instance (make sure you have SSH key and correct access)
ssh -i /path/to/your-key.pem ec2-user@your-ec2-public-ip << 'EOF'

# Update package list and install Docker if necessary
sudo yum update -y
sudo amazon-linux-extras install docker -y
sudo service docker start
sudo usermod -a -G docker ec2-user

# Pull the latest Docker image
docker pull myapp:latest

# Stop any running containers (if any)
docker stop $(docker ps -q -f ancestor=myapp)

# Remove old containers (optional)
docker rm $(docker ps -a -q -f ancestor=myapp)

# Run the container with appropriate environment variables
docker run -d -p 80:8000 \
  -e DJANGO_SECRET_KEY="$DJANGO_SECRET_KEY" \
  -e DJANGO_DEBUG="$DJANGO_DEBUG" \
  -e DATABASE_URL="$DATABASE_URL" \
  -e ALLOWED_HOSTS="$ALLOWED_HOSTS" \
  myapp:latest

EOF


