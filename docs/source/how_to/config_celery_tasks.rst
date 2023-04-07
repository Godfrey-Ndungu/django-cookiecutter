Change Celery Task Name in cookiecutter.celery and Updating Docker Compose celery_worker Command
=================================================================================================

This guide will walk you through the steps to change the Celery task name in `cookiecutter.celery` and update Docker Compose `celery_worker` command.

Step 1: Rename the Celery Task Name

First, rename the Celery task name from `tasks.example` to your desired name in `celery.py` file:

.. code-block:: python

    app.conf.task_default_queue = 'default'
    app.conf.task_default_exchange_type = 'topic'
    app.conf.task_default_routing_key = 'default'

    app.conf.task_routes = {
        'new_task': {'queue': 'new_task_queue', 'routing_key': 'new_task'},
        'example': {'queue': 'example_queue', 'routing_key': 'example'}
        # Change 'example' to your desired task name
    }

Step 2: Update Docker Compose celery_worker Command

Next, update the Docker Compose `celery_worker` command in `docker-compose.yml` file to use the new Celery task name:

.. code-block:: yaml

    version: '3'

    services:
      app:
        build:
          context: .
        command: >
          sh -c "python manage.py migrate &&
          python manage.py runserver 0.0.0.0:8000"
        ports:
          - "8000:8000"
        depends_on:
          - db
          - redis
          - celery_worker
        environment:
          - DB_HOST=db
          - REDIS_URL=redis://redis:6379/0

      celery_worker:
        build:
          context: .
        command: >
          sh -c "celery -A myproject worker -l info -Q new_task_queue,example_queue"  # Change 'example' to your new task name
        depends_on:
          - db
          - redis
        environment:
          - DB_HOST=db
          - REDIS_URL=redis://redis:6379/0

      db:
        image: postgres:12-alpine
        environment:
          POSTGRES_USER: myproject
          POSTGRES_PASSWORD: myproject
          POSTGRES_DB: myproject

      redis:
        image: redis:5-alpine

Step 3: Restart Docker Compose Services

Finally, restart the Docker Compose services to apply the changes:

.. code-block:: bash

    docker-compose down
    docker-compose up --build
