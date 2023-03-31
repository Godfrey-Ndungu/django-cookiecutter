TimestampedModel
================

The `TimestampedModel` is an abstract model that extends the `TrackableModel` and adds additional fields for timestamps. It includes the following fields:

- `date_added`: A `DateTimeField` that automatically stores the date and time when the instance is created.
- `date_updated`: A `DateTimeField` that automatically stores the date and time when the instance is updated.
- `date_deleted`: A `DateTimeField` that stores the date and time when the instance is deleted.

.. autoclass:: core.models.TimestampedModel
   :members:
   :inherited-members:
