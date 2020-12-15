#!/usr/bin/env bash
python /books/server/manage.py makemigrations
python /books/server/manage.py migrate

python /books/server/manage.py upload_file books
python /books/server/manage.py upload_file reviews

python /books/server/manage.py runserver  0.0.0.0:8000