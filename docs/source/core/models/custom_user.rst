Custom User Model for Email Code Authentication
===============================================

The `core` app provides a custom user model for email code authentication. This model, `CustomUser`, includes the `email` and `verification_code` fields, and is designed to work with Django's built-in authentication system.

Usage
-----

To use the `CustomUser` model, you'll need to add the `core` app to your Django project's `INSTALLED_APPS` setting:

.. code-block:: python

    # settings.py

    INSTALLED_APPS = [
        # other apps...
        'core',
    ]

You can then import the `CustomUser` model from the `core.models` module:

.. code-block:: python

    from core.models import CustomUser

Once you have imported the model, you can use it like any other Django model:

.. code-block:: python

    # create a new user
    user = CustomUser.objects.create_user(email='user@example.com', verification_code='1234', password='password')

    # authenticate a user
    user = authenticate(email='user@example.com', verification_code='1234')

    # get the currently logged-in user
    user = request.user

Testing
-------

The `core` app also includes tests for the `CustomUser` model, which can be run with Django's test runner:

.. code-block:: bash

    python manage.py test core.tests.CustomUserModelTest

These tests ensure that the model's fields and methods work as expected, and that a `ValidationError` is raised when attempting to create a user with a duplicate email address.
