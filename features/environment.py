from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import connection


def before_all(context):
    databases = settings.DATABASES
    database = databases.get("default", {})
    if (
        set(databases) != {"default"}
        or database.get("ENGINE") != "django.db.backends.sqlite3"
        or not connection.creation.is_in_memory_db(database.get("NAME", ""))
        or database.get("TEST", {}).get("NAME") != ":memory:"
    ):
        raise ImproperlyConfigured(
            "BDD requires config.settings_test and an in-memory SQLite database."
        )
