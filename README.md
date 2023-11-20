# Todo list app with weather

Author: Mateusz Cisek

## Prerequisites

* Docker and Docker-Compose must be installed in the system.
* Internet connection is required to build and fetch Docker images.
* For development and testing, Poetry _^1.3.0_ and Python _^3.11_ must be
  installed in the system.


## Configuration

The app can be configured using environment variables. By default, the app will
read the variables from the `.env` file that must be created prior to running
the app. Prefix `TODO_` is required for all environment variables.

All environment variables that can be used for configuration are listed
in `.env.template` file. Here is a sample configuration that can be used to run
the app:

```bash
TODO_DEBUG=true
TODO_LOGGING_LEVEL=debug
TODO_PUBLIC_HOST=localhost
TODO_SECRET_KEY="sample-very-very-long-secret-key"
TODO_STATIC_FILES_DIR=/home/user/static
TODO_TIMEZONE=Europe/London

TODO_DATABASE_HOST=database
TODO_DATABASE_PORT=5432
TODO_DATABASE_USER=todo_app
TODO_DATABASE_PASSWORD=todo_app
TODO_DATABASE_NAME=todo_app

TODO_DOCUMENT_STORE_HOST=document_store
TODO_DOCUMENT_STORE_PORT=27017
TODO_DOCUMENT_STORE_USER=todo_app
TODO_DOCUMENT_STORE_PASSWORD=todo_app
TODO_DOCUMENT_STORE_NAME=todo_app

TODO_CACHE_HOST=cache
TODO_CACHE_PORT=6379

TODO_WEATHER_API_KEY="a valid Weather API key"
```

The application will fail to start if the configuration options are not set.


## Running in production mode

To run the app in production mode, execute the following command:

```bash
docker-compose up
```

The application will be available at http://localhost:8080/.

In production mode, nginx proxy is used to serve the static files, and the
debug mode is disabled regardless of the value of the `TODO_DEBUG` environment
variable.


## Running in development mode

To run the app in development mode, execute the following command:

```bash
docker-compose -f docker-compose.dev.yaml up
```

The application will be available at http://localhost:8080/.

In development mode, the web app will reload each time the source code is
updated. The Celery worker WILL NOT reload and to apply the changes, it needs to
be restarted.


## Development environment and testing

To create the development environment and install the dependencies, execute the
following command:

```bash
poetry install
```

Once this is done, it's possible to run the tests with the following command:

```bash
poetry run pytest
```


## App description

This application allows creating tasks. Each task has a location assigned to it.
The weather for all active tasks is refreshed every minute. The web app reloads
every minute to display updated weather changes.

The content and location for each task can be updated. Each task can be marked
as active or finished.


## Structure

This is a Django project. It consists of a few parts:

* Web app (Django),
* Relational database (PostgreSQL) - it's used to store Django data,
* Document store (MongoDB) - used to store the tasks,
* Cache (Redis) - used by Celery as the tasks' queue,
* Celery worker - it updates the weather for all active tasks.


## Web app details

There are three views available:

* The list of the tasks (`/todo/`),
* View for creating a new task (`/todo/create/`),
* View for updating a task (`/todo/edit/{task id}`).

Two additional views are used for marking the tasks as active or finished
(`/todo/mark-as-active/{task id}` and `/todo/mark-as-finished/{task id}`).

Every 60 seconds, the worker updates the weather for all active tasks. New tasks
will not have any color until the first update is finished.

The tasks are coloured in the following way:

* if the temperature < 0 degrees C or the weather is "Rain" - blue,
* if the temperature is between 0 and 15 degrees C, or the weather is "Clouds" -
  orange,
* if the temperature >= 15 degrees C or the weather is "Clear" (which means no
  clouds) - red.

While adding a new task, it's required to set the content and the location for
it. The locations are also fetched from the Weather API, and it's necessary
to type at least 3 characters for it to fetch the list of available locations
(the list is limited to 5 records).

The Python code has been formatted with _black_ and _ruff_, _pytest_ has
been used for tests, and _Pydantic_ validates the configuration.


## Frontend part

The frontend part of the app has been built with Bootstrap 5, and the
interactive location field uses jQuery and select2 libraries.

For real-world projects, I would have used a React, Angular, or other JavaScript
framework.


## Limitations

The weather for each task is updated in a separate request. It may be the case
that for large amount of tasks the Weather API limit will be exceeded and the
weather update will not work.

The website with the list of tasks reloads every minute to display up-to-date
weather data. A better way to do it could be eg. WebSockets.

Github CI/CD configuration has not been added 
