import os

from django.core.asgi import get_asgi_application

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "cybersmart_assessment.core.settings.default",
)

application = get_asgi_application()