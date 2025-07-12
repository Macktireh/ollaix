ARG PYTHON_BASE=3.13.5-slim-bookworm

# base image for Python
FROM docker.io/python:$PYTHON_BASE AS python_image

#############################################################################################
# -------------------------------------- build stage -------------------------------------- #
#############################################################################################
FROM python_image AS builder

# set work directory
WORKDIR /project

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  # psycopg dependencies
  libpq-dev && \
  # install PDM
  pip install -U pdm

ENV PDM_CHECK_UPDATE=false

COPY pyproject.toml pyproject.toml
COPY pdm.lock pdm.lock

# install dependencies and project into the local packages directory
RUN pdm install --prod --no-editable

#############################################################################################
# -------------------------------------- final stage -------------------------------------- #
#############################################################################################
FROM python_image AS final

WORKDIR /project

RUN addgroup --system app && adduser --system --group app

COPY --from=builder --chown=app:app project/.venv /.venv

USER app

ENV PATH="/.venv/bin:$PATH" \
  PYTHONPATH="/project"

EXPOSE 8000

ENTRYPOINT ["python", "main.py"]
