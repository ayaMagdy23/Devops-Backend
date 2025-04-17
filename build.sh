#!/bin/bash

# Set Python version for mise (or asdf if used behind the scenes)
mise settings set python_compile 1
mise use -g python@3.11

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Build script executed successfully!"
