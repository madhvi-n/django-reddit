from .base import *

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Development database (SQLite)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

# Development email settings
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# CORS settings for development
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://localhost:4200",
]
