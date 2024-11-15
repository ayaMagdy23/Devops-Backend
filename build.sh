#!/bin/bash

# Ensure you're using the correct Python version (optional if you're using a virtual environment)
python --version

# Create a virtual environment (optional, if you're not using an existing one)
python -m venv venv
source venv/bin/activate

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Collect static files (if your app uses static files like CSS/JS)
python manage.py collectstatic --noinput

# Run database migrations (ensure that your database is set up)
python manage.py migrate
