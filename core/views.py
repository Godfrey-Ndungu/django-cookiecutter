from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse


def custom_exception_handler(exc, context):
    """
    Custom exception handler to handle PermissionDenied
    and ObjectDoesNotExist exceptions.
    """
    if isinstance(exc, PermissionDenied):
        return Response(
            {"detail": "You do not have permission to perform this action."},
            status=status.HTTP_403_FORBIDDEN,
        )

    if isinstance(exc, ObjectDoesNotExist):
        return Response(
            {"detail": "The requested resource does not exist."},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Let DRF handle other exceptions
    response = exception_handler(exc, context)

    if (
        response is not None
        and response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    ):
        # Customize error message for 500 errors
        response.data = {"detail": "Internal server error occurred."}

    return response


def handler404(request, *args, **argv):
    response_data = {
        "error": {
            "message": "The page you requested could not be found.",
            "code": 404,
            "description":
                "The URL you entered was incorrect or the page has been removed or moved.", # noqa
        }}
    response_headers = {"WWW-Authenticate":
                        'Basic realm="api"'}
    return JsonResponse(
        response_data,
        status=status.HTTP_400_BAD_REQUEST,
        headers=response_headers)


def handler500(request, *args, **argv):
    response_data = {
        "error": {
            "message": "Something went wrong on our server.",
            "code": 500,
            "description": "Server error",
        }
    }

    response_headers = {"WWW-Authenticate":
                        'Basic realm="api"'}
    return JsonResponse(
        response_data,
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        headers=response_headers,
    )
