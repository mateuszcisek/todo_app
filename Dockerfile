FROM python:3.11-alpine as python-base
LABEL maintainer="mateuszcisek@hotmail.com"

ENV HOME_DIRECTORY="/home/user" \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_NO_CACHE_DIR=off \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=1.3.0 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    PYSETUP_PATH="/opt/pysetup" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    USERNAME="user" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


########## builder-base ########################################################
FROM python-base as builder-base

RUN apk update \
    && apk add curl g++ make libpq-dev libffi-dev binutils \
    && curl -sSL https://install.python-poetry.org | python -

WORKDIR "${PYSETUP_PATH}"
COPY poetry.lock pyproject.toml .
RUN poetry install --no-dev --no-root


########## development #########################################################
FROM python-base as development

RUN apk update \
    && apk add curl g++ make libpq-dev libffi-dev binutils \
    && curl -sSL https://install.python-poetry.org | python - \
    && adduser -D -h "${HOME_DIRECTORY}" "${USERNAME}" "${USERNAME}"

COPY --from=builder-base "${POETRY_HOME}" "${POETRY_HOME}"
COPY --from=builder-base "${PYSETUP_PATH}" "${PYSETUP_PATH}"

WORKDIR "${PYSETUP_PATH}"
RUN poetry install --no-root \
    && mkdir -p "${HOME_DIRECTORY}/app" \
    && chown -R "${USERNAME}:${USERNAME}" "${HOME_DIRECTORY}"

WORKDIR "${HOME_DIRECTORY}/app/"
USER "${USERNAME}"
EXPOSE 8000

CMD ["python", "manage.py", "runserver"]


########## production ##########################################################
FROM python-base as production

COPY --from=builder-base "${PYSETUP_PATH}" "${PYSETUP_PATH}"

RUN apk update \
    && apk add curl g++ make libpq-dev libffi-dev binutils \
    && adduser -D -h "${HOME_DIRECTORY}" "${USERNAME}" "${USERNAME}" \
    && mkdir -p "${HOME_DIRECTORY}/app" "${HOME_DIRECTORY}/static" \
    && chown -R "${USERNAME}:${USERNAME}" "${HOME_DIRECTORY}"

WORKDIR "${HOME_DIRECTORY}/app/"

COPY src/todo_app/ todo_app
COPY manage.py .

USER "${USERNAME}"
EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--threads", "4", "todo_app.core.wsgi:application"]
