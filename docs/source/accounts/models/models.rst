=====================
Models
=====================

CustomUserManager and CustomUser
=================================

The **CustomUserManager** and **CustomUser** models in the **apps.accounts.models** 
file are designed to extend the default Django user model with additional functionality and customizations.

To understand how these models work, let's start by examining the **CustomUserManager** model. 
This model is responsible for creating and managing instances of the **CustomUser** model. 
It overrides the default Django BaseUserManager to provide custom functionality. 
Specifically, the **CustomUserManager** model provides two additional methods:

* **create_user()**: This method creates a new user instance using the provided email and password. It sets the is_staff and is_superuser attributes to False, indicating that this is a regular user account.
* **create_superuser()**: This method creates a new user instance with the provided email and password, but sets the is_staff and is_superuser attributes to True. This indicates that this is an administrator account with elevated privileges.

The CustomUser model itself extends the default Django **AbstractBaseUser** and **PermissionsMixin** models to provide additional customizations. 
It defines several fields, including email, first_name, and last_name. It also defines two boolean fields, is_active and is_staff, which determine whether the user account is currently active and whether the user has staff permissions, respectively.

To use these models in your Django project, you'll first need to import **CustomUSer** into your file. You can do this using the following code:

.. code-block:: python

    from apps.accounts.models  import CustomUser

    user = CustomUser.objects.create_user(email = 'user@example.com', password = 'password* **23')
    admin = CustomUser.objects.create_superuser(email = 'admin@example.com', password = 'password* **23')


UserVisitHistory
======================
The **UserVisitHistory** model in the **apps.accounts.models** module is used to store the visit history of users in your application.
This model is particularly useful if you want to keep track of which pages or sections of your app users are visiting, 
how often they visit, and when they last visited.

The structure of the UserVisitHistory model consists of the following fields:

* **user**: A foreign key to the user who made the visit.
* **timestamp**: The date and time of the visit.
* **url**: The URL of the page visited.
* **referer**: The URL of the referring page, if any.
* **user_agent**: The user agent string for the browser or other client used to make the visit.

To use these models in your Django project, you'll first need to import **CustomUSer** into your file. You can do this using the following code:

.. code-block:: python

    from apps.accounts.models import UserVisitHistory
    
    user = CustomUser.objects.get(id=* **)
    UserVisitHistory.objects.create(
        user=user,
        url='/example',
        referer=None,
        user_agent='Mozilla/5.0 (Windows NT * **0.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.* **0 Safari/537.3'
    )

To retrieve user visit history records, you can use the objects manager of the UserVisitHistory model:

.. code-block:: python

    from django.utils import timezone
    from apps.accounts.models import CustomUSer
    from apps.accounts.models import UserVisitHistory

    # Get all user visit history records for a specific user
    user = CustomUser.objects.get(id=* **)
    visit_history = UserVisitHistory.objects.filter(user=user)

    # Get all user visit history records for a specific URL
    visit_history = UserVisitHistory.objects.filter(url='/example')

    # Get all user visit history records for a specific time range
    start_time = timezone.now() - timezone.timedelta(days=7)
    end_time = timezone.now()
    visit_history = UserVisitHistory.objects.filter(timestamp__range=(start_time, end_time))

LoginHistoryTrail
===================
**LoginHistoryTrail** is a model that stores a trail of login attempts made by users. 
It is a part of the apps.accounts.models module. This model has the following fields:

* **user**: A foreign key to the user who made the login attempt.
* **timestamp**: The date and time of the login attempt.
* **successful**: A boolean field indicating whether the login attempt was successful or not.
* **ip_address**: The IP address used to make the login attempt.
* **user_agent**: The user agent string for the browser or other client used to make the login attempt.
* **location**: The location (city, country) of the IP address used to make the login attempt, if available.

To use this model in your Django project, you need to follow these steps:

.. code-block:: python
    
    from apps.accounts.models import LoginHistoryTrail

    LoginHistoryTrail.objects.create(user=user, ip_address=ip_address, user_agent=user_agent, location=location, successful=successful)

To retrieve login history trail records, you can use the objects attribute of the LoginHistoryTrail model:

.. code-block:: python

    from apps.accounts.models import LoginHistoryTrail

    LoginHistoryTrail.objects.create(user=user, ip_address=ip_address, user_agent=user_agent, location=location, successful=successful)

LoginAttemptHistory
=====================

The **LoginAttemptHistory** model is a Django model used to store a history of login attempts made by users . This model is located in the **apps.accounts.models**

Fields:

* **user**: A foreign key to the CustomUser model representing the user who made the login attempt.
* **timestamp**: The date and time of the login attempt, automatically generated when a new instance is created.
* **successful**: A boolean field indicating whether the login attempt was successful or not.
* **ip_address**: The IP address used to make the login attempt, stored as a GenericIPAddressField.
* **user_agent**: The user agent string for the browser or other client used to make the login attempt, stored as a TextField.
* **location**: The location (city, country) of the IP address used to make the login attempt, if available, stored as a CharField.

Usage:
To use the LoginAttemptHistory model, you can import it in any Django file using the from apps.accounts.models import LoginAttemptHistory statement.

To create a new LoginAttemptHistory instance, you can call its constructor and pass the necessary arguments as follows:

.. code-block:: python

    from apps.accounts.models import LoginAttemptHistory
    from apps.accounts.models import CustomUser
    from django.utils import timezone

    user = CustomUser.objects.get(email='example@example.com')
    ip_address = '* **27.0.0.* **'
    user_agent = 'Mozilla/5.0 (Windows NT * **0.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.* **0 Safari/537.3'

    # create new instance
    login_attempt = LoginAttemptHistory(
        user=user,
        successful=False,
        ip_address=ip_address,
        user_agent=user_agent,
        location=None
    )

    # save instance to database
    login_attempt.save()


To retrieve all login attempts for a particular user, you can use Django's related manager:

.. code-block:: python

    from apps.accounts.models import CustomUser
    from apps.accounts.models import LoginAttemptHistory

    user = CustomUser.objects.get(email='example@example.com')
    login_attempts = user.loginattempthistory_set.all()

To retrieve all successful login attempts for a particular user:

.. code-block:: python

    from apps.accounts.models import CustomUser
    from apps.accounts.models import LoginAttemptHistory

    user = CustomUser.objects.get(email='example@example.com')
    successful_login_attempts = user.loginattempthistory_set.filter(successful=True)


ExtraData
=============
The **ExtraData** model is used to store additional information related to user activity, 
such as browser information, IP address, device details, operating system, and location. 
This information can be useful for tracking user activity and analyzing user behavior
on your website or application.


Fields

* **user (ForeignKey)**: A foreign key to the CustomUser model, indicating which user this extra data belongs to. 
* **timestamp (DateTimeField)**: A date and time field indicating when this extra data was recorded. This field is set to auto_now_add, meaning it will automatically be set to the current date and time when a new record is created.
* **browser (CharField)**: A string field that stores the user's browser information.
* **ip_address (GenericIPAddressField)**: A field that stores the user's IP address. This field automatically validates the input to ensure it is a valid IP address.
* **device (CharField)**: A string field that stores the user's device details.
* **os (CharField)**: A string field that stores the user's operating system.
* **location (CharField)**: A string field that stores the user's location information.

To use the ExtraData model, you can create a new record whenever you want to 
store additional information related to user activity.

.. code-block:: python

    from apps.accounts.models import ExtraData
    from apps.accounts.models import CustomUser

    # Assume that we have a user object representing the current user
    current_user = CustomUser.objects.get(id=1)

    # Create a new ExtraData record
    extra_data = ExtraData.objects.create(
        user=current_user,
        browser='Chrome',
        ip_address='192.168.0.1',
        device='Desktop',
        os='Windows 10',
        location='New York'
    )

    # The timestamp field will be set automatically by the auto_now_add argument in the model definition.


OTP
========
The **OTP** model is used to store one-time passwords (OTPs) associated with a 
user in the CustomUser model. This model is defined in the apps.accounts.models module.

Fields

* **user (ForeignKey)**: The user associated with the OTP. This field is required.
* **code (CharField)**: The OTP code. This field is unique and has a maximum length of 4 characters. This field is required.
* **active (BooleanField)**: A boolean indicating whether the OTP is active or not. By default, this field is set to True.
* **created_at (DateTimeField)**: The date and time when the OTP was created. This field is automatically set when the OTP is created.
* **updated_at (DateTimeField)**: The date and time when the OTP was last updated. This field is automatically set when the OTP is saved.

Methods

* **create()**: Creates a new OTP for the given user and returns it.
* **get_latest()**: Gets the latest active OTP for the given user or returns None.
* **is_valid()**: Checks whether or not the OTP is valid (i.e. active and not expired) and returns a boolean value.
* **save()**: Saves the OTP to the database after validating the code is a 4-digit number or raises a ValidationError.

To create a new OTP for a user, call the OTP.create() method and pass in the user as an argument:

.. code-block:: python

    from accounts.models import CustomUSer
    from accounts.models import OTP

    user = CustomUser.objects.get(pk=1)
    otp = OTP.create(user)

To get the latest active OTP for a user, call the **OTP.get_latest()**
method and pass in the user as an argument:

.. code-block:: python

    from accounts.models import CustomUSer
    from accounts.models import OTP

    user = CustomUser.objects.get(pk=1)
    otp = OTP.get_latest(user)

To check if an OTP is valid, call the is_valid() method on an instance of the OTP model:

.. code-block:: python

    if otp.is_valid():
        # The OTP is valid
    else:
        # The OTP is invalid
