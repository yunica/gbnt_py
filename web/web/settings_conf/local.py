from .common import *

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": environ.get("POSTGRES_DB", "postgres"),
        "USER": environ.get("POSTGRES_USER", "postgres"),
        "PASSWORD": environ.get("POSTGRES_PASSWORD", "postgres"),
        "HOST": environ.get("DATABASE_HOST", "localhost"),
        "PORT": environ.get("POSTGRES_PORT", "5432"),
        "CONN_MAX_AGE": 60,
    }
}

# static
STATICFILES_DIRS = [
    f"{BASE_DIR}/static",
]
MEDIA_ROOT = f"{BASE_DIR}/media"

STATIC_URL = "/static/"
MEDIA_URL = "/media/"

# coors
CORS_ALLOW_ALL_ORIGINS = True
