TrackableModel
==============

The `TrackableModel` is an abstract model that tracks changes to the model instances. It includes the following fields:

- `created_at`: A `DateTimeField` that automatically stores the date and time when the instance is created.
- `updated_at`: A `DateTimeField` that automatically stores the date and time when the instance is updated.
- `created_by`: A `ForeignKey` that stores the user who created the instance.
- `updated_by`: A `ForeignKey` that stores the user who updated the instance.
- `history`: A `JSONField` that stores the history of changes to the instance.

The `TrackableModel` also includes a custom `save` method that updates the `history` field whenever an instance is saved.

.. autoclass:: core.models.TrackableModel
   :members:
   :exclude-members: save
   :inherited-members:
