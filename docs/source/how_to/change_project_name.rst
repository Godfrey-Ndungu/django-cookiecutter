Change the Django Project Name from "cookiecutter" to a Desired Name
======================================================================

This guide will walk you through the steps to change the Django project name from "cookiecutter" to a desired name.

Step 1: Rename the Project Directory

First, rename the project directory from "cookiecutter" to your desired name:

.. code-block:: bash

    mv cookiecutter/ myproject/

Step 2: Update the Project Name in Files

Next, update the project name in the following files:

- `myproject/settings/base.py`: Change the `ROOT_URLCONF` to the new URL conf module.
- `myproject/wsgi.py`: Change the `DJANGO_SETTINGS_MODULE` to the new settings module.
- `myproject/asgi.py`: Change the `DJANGO_SETTINGS_MODULE` to the new settings module.
- `manage.py`: Change the `DJANGO_SETTINGS_MODULE` to the new settings module.
- `myproject/settings.py`: Change the `DEFAULT_FILE_STORAGE` to the new settings module.

Step 3: Update the Project Name in Docker and Docker Compose Files

If you are using Docker and Docker Compose, update the project name in the following files:

- `docker-compose.yml`: Change the `services.app.container_name` to the new container name.
- `docker-compose.prod.yml`: Change the `services.app.container_name` to the new container name.
- `Dockerfile`: Change the `WORKDIR` and `COPY` commands to reflect the new project directory name.

Step 4: Update the Project Name in AWS Configs

If you are using AWS, update the project name in the following files:

- `backend/settings.py`: Change the `ROOT_URLCONF` to the new URL conf module.

Step 5: Conclusion

You have now successfully changed the Django project name from "cookiecutter" to your desired name.
