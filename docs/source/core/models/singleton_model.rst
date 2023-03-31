SingletonModel
==============

The `SingletonModel` is an abstract model that provides functionality for only allowing a single instance of a model to be created. It includes the following field:

- `singleton_id`: A `PositiveIntegerField` that stores the ID of the singleton instance. This field should always have a value of 1.

The `SingletonModel` also includes a custom `save` method that overrides the default behavior to prevent multiple instances from being created. It also includes a `load` method that returns the singleton instance of the model.

.. autoclass:: core.models.SingletonModel
   :members: save, load
   :special-members: __doc__
   :inherited-members:
