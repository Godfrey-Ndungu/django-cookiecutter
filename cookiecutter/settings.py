from split_settings.tools import optional, include
from decouple import config

include(
    "components/base.py",
)

#     # # aws settings cloudfront
AWS_ACCESS_KEY_ID = (config("AWS_ACCESS_KEY_ID"),)
AWS_SECRET_ACCESS_KEY = (config("AWS_SECRET_ACCESS_KEY"),)
AWS_STORAGE_BUCKET_NAME = (config("AWS_STORAGE_BUCKET_NAME"),)
AWS_QUERYSTRING_AUTH = (config("AWS_QUERYSTRING_AUTH"),)
AWS_DEFAULT_ACL = (config("AWS_DEFAULT_ACL"),)
AWS_S3_SIGNATURE_VERSION = (config("AWS_S3_SIGNATURE_VERSION"),)
AWS_S3_OBJECT_PARAMETERS = (config("AWS_S3_OBJECT_PARAMETERS"),)
PUBLIC_MEDIA_LOCATION = (config("PUBLIC_MEDIA_LOCATION"),)
DEFAULT_FILE_STORAGE = ("cookiecutter.storage_backends.PublicMediaStorage",)
MEDIAFILES_LOCATION = (config("MEDIAFILES_LOCATION"),)
MEDIA_ROOT = f"/{MEDIAFILES_LOCATION}/"
AWS_CLOUDFRONT_DOMAIN = (config("AWS_CLOUDFRONT_DOMAIN"),)
MEDIA_URL = f"//{AWS_CLOUDFRONT_DOMAIN}/{MEDIAFILES_LOCATION}/"

CELERY_BROKER_URL = "redis://redis:6379"
CELERY_RESULT_BACKEND = "redis://redis:6379"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT"),
    }
}