Replace Redis with RabbitMQ
=============================

This guide will walk you through the steps to replace Redis with RabbitMQ as the message broker in your Django project.

Step 1: Install RabbitMQ

First, you need to install RabbitMQ. You can follow the official documentation for installation instructions: https://www.rabbitmq.com/download.html

Step 2: Install the Required Packages

Next, you need to install the required packages to use RabbitMQ as the message broker. You can install the `pika` package with pip:

.. code-block:: bash

    pip install pika

Step 3: Update the Celery Configuration

Update the Celery configuration in `celery.py` file to use RabbitMQ as the message broker:

.. code-block:: python

    from kombu import Exchange, Queue

    broker_url = 'amqp://guest:guest@localhost:5672//' # Change this to your RabbitMQ URL

    task_queues = (
        Queue('default', Exchange('default'), routing_key='default'),
        Queue('new_task_queue', Exchange('new_task'), routing_key='new_task'),
    )

    task_routes = {
        'new_task': {'queue': 'new_task_queue', 'routing_key': 'new_task'},
    }

Step 4: Update the Docker Compose Configuration

Update the Docker Compose configuration in `docker-compose.yml` file to use RabbitMQ instead of Redis:

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
          - rabbitmq
          - celery_worker
        environment:
          - DB_HOST=db
          - BROKER_URL=amqp://guest:guest@rabbitmq:5672//" # Change this to your RabbitMQ URL

      celery_worker:
        build:
          context: .
        command: >
          sh -c "celery -A myproject worker -l info -Q new_task_queue" 
        depends_on:
          - db
          - rabbitmq
        environment:
          - DB_HOST=db
          - BROKER_URL=amqp://guest:guest@rabbitmq:5672//" # Change this to your RabbitMQ URL

      db:
        image: postgres:12-alpine
        environment:
          POSTGRES_USER: myproject
          POSTGRES_PASSWORD: myproject
          POSTGRES_DB: myproject

      rabbitmq:
        image: rabbitmq:3.9-alpine

Step 5: Restart Docker Compose Services

Finally, restart the Docker Compose services to apply the changes:

.. code-block:: bash

    docker-compose down
    docker-compose up --build

Conclusion
----------

You have now successfully replaced Redis with RabbitMQ as the message broker in your Django project.
