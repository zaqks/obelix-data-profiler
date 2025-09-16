#!/usr/bin/env bash
set -o errexit  # Exit on errors

# Create virtual environment in .venv if it doesn't exist
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

# Activate the virtual environment
source .venv/bin/activate

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt --ignore-requires-python

# Collect static files without interactive input
# python manage.py collectstatic --no-input

# # Apply any pending migrations
# python manage.py migrate

echo "Build and deployment steps completed."
