import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "todo_app.core.settings.default",
)

application = get_wsgi_application()
