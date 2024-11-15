#!/bin/bash

# Activate the virtual environment if you are using one
source venv/bin/activate

# Run unit tests using Django's test framework
python manage.py test

# Optionally run linting or code style checks
flake8 .

# If you're using coverage reporting, you can include:
# coverage run manage.py test
# coverage report
