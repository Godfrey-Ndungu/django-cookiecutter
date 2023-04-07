Customize Django Rest Errors
===============================

This guide will walk you through the steps to customize the error handling in Django Rest using a custom exception handler.

Step 1: Create a Custom Exception Handler

Create a new file `custom_error_handlers.py` in your `core/views/` directory, and add the following code:

.. code-block:: python

    from django.core.exceptions import ObjectDoesNotExist
    from rest_framework.exceptions import PermissionDenied
    from rest_framework.views import exception_handler
    from rest_framework.response import Response
    from rest_framework import status

    def custom_exception_handler(exc, context):
        """
        Custom exception handler to handle PermissionDenied and ObjectDoesNotExist exceptions.
        """
        if isinstance(exc, PermissionDenied):
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        
        if isinstance(exc, ObjectDoesNotExist):
            return Response({"detail": "The requested resource does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Let DRF handle other exceptions
        response = exception_handler(exc, context)

        if response is not None and response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
            # Customize error message for 500 errors
            response.data = {"detail": "Internal server error occurred."}

        return response

Step 2: Register the Custom Exception Handler

Add the `custom_exception_handler` to the `EXCEPTION_HANDLER` setting in your Django settings file:

.. code-block:: python

    REST_FRAMEWORK = {
        'EXCEPTION_HANDLER': 'core.views.custom_error_handlers.custom_exception_handler'
    }

Step 3: Test the Custom Exception Handler

Test the custom exception handler by triggering an exception in your Django Rest API. For example, if you try to access a non-existent object, you should see the custom error message "The requested resource does not exist."
