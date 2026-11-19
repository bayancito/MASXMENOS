"""Isolated BDD settings with an ephemeral SQLite database."""

from .settings import *  # noqa: F403

SECRET_KEY = "masxmenos-isolated-tests-only"
DEBUG = False
ALLOWED_HOSTS = ["testserver", "localhost", "127.0.0.1"]

# Replace every database alias before Django initializes any connection.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "TEST": {"NAME": ":memory:"},
    }
}
DATABASE_ROUTERS = []

INSTALLED_APPS = [*INSTALLED_APPS, "behave_django"]  # noqa: F405

# Build application tables directly from current models for this test database.
# Historical migrations contain duplicate CreateModel operations and omit models.
# Django's built-in migrations still run normally.
MIGRATION_MODULES = {
    "usuarios": None,
    "productores": None,
    "productos": None,
    "reportes": None,
}

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.InMemoryStorage"},
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
    },
}
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
