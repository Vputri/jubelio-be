# Makefile for Supermarket Analytics Project

.PHONY: help runserver import-excel test convert-html install

help:
	@echo "Available commands:"
	@echo "  make install         Install Python dependencies from requirements.txt"
	@echo "  make runserver      Run Django development server on localhost:8000"
	@echo "  make import-excel   Import data from Excel (see README for usage)"
	@echo "  make test           Run API and Django tests"
	@echo "  make convert-html   Convert markdown slides to HTML presentation"

install:
	pip install -r requirements.txt

runserver:
	python manage.py runserver

import-excel:
	python manage.py import_excel_data

test:
	python manage.py test
	python test_api.py | tee api_test_output.txt

convert-html:
	python markdown_to_html.py SLIDE_PRESENTASI.md slide_presentasi.html 