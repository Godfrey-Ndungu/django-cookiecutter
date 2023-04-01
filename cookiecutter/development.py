from split_settings.tools import include
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent
include(
    "components/base.py",
)

ALLOWED_HOSTS = ["*"]

DEBUG = True

MEDIA_URL = "/media/"
MEDIA_ROOT = "media/"

CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT"),
        "TEST": {
            "NAME": "testdb",
        },
    }
}