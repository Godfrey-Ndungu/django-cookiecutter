
.. currentmodule:: apps.core.models

============================
Introduction
==================================

The apps.core.models module contains several models that are used across the application. In this document, we will describe the TrackableModel, TimestampedModel, and Task models.

TrackableModel
===============
The TrackableModel is an abstract model that provides fields to automatically track changes and keep a record of who made them. It has the following attributes:

* **created_at (DateTimeField)**: The timestamp when the model instance was first created.\

* **updated_at (DateTimeField)**: The timestamp of the most recent update to the model instance.\

* **created_by (ForeignKey)**: The user who created the model instance.\

* **updated_by (ForeignKey)**: The user who last updated the model instance.\

* **history (JSONField)**: A JSON field that stores a complete history of changes to the model instance, including timestamps and the user who made each change.\

To use this model, you can create a new model and inherit from it:

.. code-block:: python

   from django.db import models
   from apps.accounts.models import TrackableModel

   class MyModel(TrackableModel):
      my_field = models.CharField(max_length=255)

TimestampedModel
==================
The TimestampedModel is an abstract model that builds on the functionality of TrackableModel by adding extra fields for timestamping. It has the following attributes:

* **date_added (DateTimeField)**: The timestamp when the model instance was first added.
* **date_updated (DateTimeField)**: The timestamp of the most recent update to the model instance.
* **date_deleted (DateTimeField)**: The timestamp of when the model instance was deleted (if applicable).

To use this model, you can create a new model and inherit from it:

.. code-block:: python

   from django.db import models
   from apps.core.models import TimestampedModel

   class MyModel(TimestampedModel):
      my_field = models.CharField(max_length=255)

Task
======
The Task model is used for tracking tasks. It has the following attributes:


* **name (str)**: The name of the task.
* **task_ingestor (str)**: The ingestor responsible for the task.
* **datetime (datetime)**: The date and time the task was created.
* **status (str)**: The current status of the task. Allowed values are 'pending', 'processing', 'processed', and 'failed'.

It also has the following methods:

* **start_processing()**: Transition the task from 'pending' to 'processing'.
* **complete_processing()**: Transition the task from 'processing' to 'processed' and delete the record.
* **fail_processing()**: Transition the task from 'processing' to 'failed'.

To use this model, you can create a new model and inherit from it:

.. code-block:: python

   from django.db import models
   from apps.core.models import Task

   class MyTaskModel(Task):
    my_field = models.CharField(max_length=255)
