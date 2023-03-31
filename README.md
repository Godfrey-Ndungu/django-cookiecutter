
# Django-Minimal-CookieCutter

Django minimal cookie cutter is a template or starting point for creating a new Django project with a minimal set of features and components. This cookie cutter is designed for developers who want to start with a basic Django project structure and add their own custom features as needed.


## Authors

- [@Godfrey-Ndungu](https://github.com/Godfrey-Ndungu)


## Features

1.Abstract Models:

-TrackableModel: Includes fields for creation and modification timestamps, as well as created by and modified by fields.  
-Singleton: A model that only allows one instance to be created.  
-TimestampedModel: Includes fields for creation and modification timestamps.

2.Media files:  
-On development, media files is stored locally.  
-On production, media files is stored on AWS with CloudFront.

3.Two settings:  
-One for development.  
-One for production.

4.Coverage:   
-Code coverage is measured and reported.
Automation:

5.tox is used to automate flake8, testing, and coverage reporting.  

6.A Makefile is included to help set up Python and the project locally, including installing Redis and Postgres.

7.Circle CI configs is included for the default branch development that merges to the main branch.  

8.Ansible is used to set up the project using Docker.

9.A custom error gives helpful json response when a 500 0r 404 error occurs.

10.Django REST Framework.

11.API Redoc .

12.Django Celery , with Redis configured in the project.

13.Sphinx docs is installed and configured.
Database based logging:

14.Logging is stored in the database.

15.The signal loader , so you don't have to register your signals in the app file.

16.Email support with celery background task
## Documentation

[Documentation](https://django-minimal-cookiecutter.readthedocs.io/en/latest/)


## Run Locally

Clone the project

```bash
  chmod +x makefile.sh
  ./makefile.sh
```




## Running Tests

To run tests, run the following command

```bash
  tox
```

