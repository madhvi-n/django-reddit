import os


def configure_environment():
    environment = os.getenv("ENVIRONMENT", "development").lower()

    settings_map = {
        "development": "reddit_clone.settings.development",
        "production": "reddit_clone.settings.production",
        "test": "reddit_clone.settings.test",
    }

    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        settings_map.get(environment, settings_map["development"]),
    )
