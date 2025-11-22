import os

# Simple env variable: development / production / test
ENVIRONMENT = os.getenv("ENVIRONMENT", "development").lower()

# Django settings modules
SETTINGS_MAP = {
    "development": "reddit_clone.settings.development",
    "production": "reddit_clone.settings.production",
}

settings_module = SETTINGS_MAP.get(ENVIRONMENT, SETTINGS_MAP["development"])
os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)
