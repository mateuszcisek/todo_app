from pathlib import Path

from todo_app.core.settings.default import *

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "database.sqlite",
    },
}
