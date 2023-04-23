===========================================
Using the OTP Model 
===========================================

The OTP (one-time password) model in the `core` app provides a convenient way to generate and verify OTPs for a user.
Features:
----------------

1.1. created_at field to track the date and time the OTP was created.

1.2. expires_at field to track the date and time the OTP expires.

1.3. max_attempts field to track the maximum number of attempts a user has to verify an OTP before it becomes invalid.[TODO]

1.4. attempts field to track the number of attempts a user has made to verify an OTP.[TODO]

1.5. Method to generate a new OTP only if the previous OTP has expired or the user has used up all their attempts.

1.6. Method to reset the number of attempts a user has made to verify an OTP.

Constraints:
----------------

2.1. Each user can have only one active OTP at a time.

2.2. The OTP value is unique for each user and cannot be reused.

2.3. The OTP expires after a specified time period, such as one hour.

2.4. The OTP value is a string of up to four characters.

2.5. The max_attempts field is greater than or equal to 1 to prevent users from verifying an OTP indefinitely.

2.6. The attempts field is less than or equal to the max_attempts field to prevent users from attempting to verify an OTP indefinitely.


Creating an OTP
----------------

To create an OTP for a user, you can call the `create` method on the OTP model, passing in the user object as an argument:

.. code-block:: python

    from core.models import OTP
    from django.contrib.auth.models import User

    user = User.objects.get(username='johndoe')
    otp = OTP.create(user)

This will generate a new, unique OTP for the user and mark any existing OTPs as inactive. The OTP value is a string of up to four characters.

Getting the Latest OTP
-----------------------

To get the latest OTP for a user, you can call the `get_latest_otp` method on the OTP model, passing in the user object as an argument:

.. code-block:: python

    from core.models import OTP
    from django.contrib.auth.models import User

    user = User.objects.get(username='johndoe')
    otp = OTP.get_latest_otp(user)

This will return the most recent OTP for the user.

Verifying an OTP
----------------

To verify whether an OTP is valid for a user, you can call the `verify` method on the OTP model, passing in the OTP value and the user object as arguments:

.. code-block:: python

    from core.models import OTP
    from django.contrib.auth.models import User

    user = User.objects.get(username='johndoe')
    otp_value = '1234'
    is_valid = OTP.verify(otp_value, user)

This will return a boolean value indicating whether the OTP is valid for the user.

Making Changes to the OTP Model
-------------------------------

If you need to make changes to the OTP model, you can modify the `core/models.py` file in your project's codebase. Be sure to run any necessary migrations after making changes to the model.

For more information on working with models in Django, see the `Django documentation <https://docs.djangoproject.com/en/3.2/topics/db/models/>`_.

