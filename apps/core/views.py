from rest_framework import status
from django.http import JsonResponse


def handler404(request, *args, **argv):  # pragma: no cover
    response_data = {
        "error": {
            "message": "The page you requested could not be found.",
            "code": 404,
            "description":
                "The URL you entered was incorrect or the page has been removed or moved.",  # noqa
        }}
    response_headers = {"WWW-Authenticate":
                        'Basic realm="api"'}
    return JsonResponse(
        response_data,
        status=status.HTTP_400_BAD_REQUEST,
        headers=response_headers)


def handler500(request, *args, **argv):  # pragma: no cover
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
