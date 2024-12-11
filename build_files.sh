#!/bin/bash

# Activate Python runtime provided by Vercel
if command -v python3 &>/dev/null; then
    alias python=python3
elif command -v python &>/dev/null; then
    alias python=python
else
    echo "Python is not available. Aborting."
    exit 1
fi

# Install required dependencies
python -m ensurepip --upgrade || echo "ensurepip not supported"
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput