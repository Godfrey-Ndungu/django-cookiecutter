from split_settings.tools import optional, include
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
include(
    'components/base.py',
)

ALLOWED_HOSTS = ['*']

DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(BASE_DIR / 'db.sqlite3'),
    }
}
