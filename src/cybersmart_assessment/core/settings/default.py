from cybersmart_assessment.core.config import AppConfig

config = AppConfig()

DEBUG = config.debug
SECRET_KEY = config.secret_key

ALLOWED_HOSTS = [config.public_host]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "cybersmart_assessment.todo",
    "cybersmart_assessment.system",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "cybersmart_assessment.core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "cybersmart_assessment.core.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config.database_name,
        "USER": config.database_user,
        "PASSWORD": config.database_password.get_secret_value(),
        "HOST": config.database_host,
        "PORT": config.database_port,
    }
}

DOCUMENT_STORE_HOST = config.document_store_host
DOCUMENT_STORE_PORT = config.document_store_port
DOCUMENT_STORE_USER = config.document_store_user
DOCUMENT_STORE_PASSWORD = config.document_store_password.get_secret_value()
DOCUMENT_STORE_NAME = config.document_store_name

CELERY_APP_NAME = "celeryapp"
CELERY_BROKER_URL = f"redis://{config.cache_host}:{config.cache_port}/1"
CELERY_RESULT_BACKEND = f"redis://{config.cache_host}:{config.cache_port}/2"
CELERYD_HIJACK_ROOT_LOGGER = False

CELERY_APP_CONFIGURATION = {
    "task_default_queue": "weather",
    "task_serializer": "json",
    "accept_content": ["json"],
    "result_serializer": "json",
    "timezone": config.time_zone,
    "enable_utc": True,
}
CELERY_ROUTES = {
    "system.celery.tasks.*": {"queue": "weather"},
}

WEATHER_API_KEY = config.weather_api_key

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "{asctime} | {levelname} | {message}",
            "style": "{",
        }
    },
    "handlers": {
        "console": {
            "level": config.logging_level,
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "celeryapp": {
            "handlers": ["console"],
            "level": config.logging_level,
            "propagate": True,
        },
        "celery": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": True,
        },
        "celery.task": {
            "handlers": [],
            "level": "ERROR",
            "propagate": True,
        },
    },
}

TIME_ZONE = config.time_zone
LANGUAGE_CODE = "en-us"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = config.static_files_dir

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
