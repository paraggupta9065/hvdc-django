#!/bin/bash

# Activate the virtual environment
source /var/www/html/hvdc-django/my-env/bin/activate

# Install requirements
pip install -r requirements.txt

# Run Django on 0.0.0.0:8000
python manage.py runserver 0.0.0.0:8000
