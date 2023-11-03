ARG PYTHON_VERSION=3.11.1-slim-bullseye

# define an alias for the specfic python version used in this file.
FROM python:${PYTHON_VERSION} as python

# Python build stage
FROM python as python-build-stage


# Install apt packages
RUN apt-get update && apt-get install --no-install-recommends -y git

# Requirements are installed here to ensure they will be cached.
COPY requeriments.txt .

# Create Python Dependency and Sub-Dependency Wheels.
RUN pip wheel --wheel-dir /usr/src/app/wheels  \
  -r requeriments.txt


# Python 'run' stage
FROM python as python-run-stage

ARG APP_HOME=/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# copy application code to WORKDIR
COPY src ${APP_HOME}

WORKDIR ${APP_HOME}

# Install required system dependencies
#RUN apt-get update && apt-get install --no-install-recommends -y \
  # cleaning up unused files
#  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
#  && rm -rf /var/lib/apt/lists/*

# All absolute dir copies ignore workdir instruction. All relative dir copies are wrt to the workdir instruction
# copy python dependency wheels from python-build-stage
COPY --from=python-build-stage /usr/src/app/wheels  /wheels/

# use wheels to install python dependencies
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
	&& rm -rf /wheels/

COPY docker/start .

ENTRYPOINT ["/app/start"]
