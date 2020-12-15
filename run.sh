#!/usr/bin/env bash
python /book_search/server/manage.py upload_file books
python /book_search/server/manage.py upload_file reviews
python /book_search/server/manage.py runserver  0.0.0.0:8000