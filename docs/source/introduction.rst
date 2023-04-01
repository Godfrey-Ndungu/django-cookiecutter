Introduction
============================

Django minimal cookie cutter is a template or starting point for creating a new Django project with a minimal set of features and components. This cookie cutter is designed for developers who want to start with a basic Django project structure and add their own custom features as needed.

Features
--------

The following features are included in the Django-Minimal-CookieCutter:

- Abstract Models:
  - TrackableModel: Includes fields for creation and modification timestamps, as well as created by and modified by fields.
  - Singleton: A model that only allows one instance to be created.
  - TimestampedModel: Includes fields for creation and modification timestamps.
- Media files:
  - On development, media files are stored locally.
  - On production, media files are stored on AWS with CloudFront.
- Two settings:
  - One for development.
  - One for production.
- Coverage:
  - Code coverage is measured and reported.
- Automation:
  - Tox is used to automate flake8, testing, and coverage reporting.
  - A Makefile is included to help set up Python and the project locally, including installing Redis and Postgres.
  - Circle CI configs is included for the default branch development that merges to the main branch.
  - Ansible is used to set up the project using Docker.
  - A custom error gives helpful JSON response when a 500 or 404 error occurs.
- Django REST Framework.
  - API Redoc.
- Django Celery, with Redis configured in the project.
- Sphinx docs is installed and configured.
- Database based logging: Logging is stored in the database.
- The signal loader, so you don't have to register your signals in the app file.
- Email support with Celery background task.
