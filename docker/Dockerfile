# syntax=docker/dockerfile:1

# Stage 1: General debian environment
FROM debian:stable-slim AS linux-base

# Assure UTF-8 encoding is used.
ENV LC_CTYPE=C.utf8
# Location of the virtual environment
ENV UV_PROJECT_ENVIRONMENT="/venv"
# Location of the python installation via uv
ENV UV_PYTHON_INSTALL_DIR="/python"
# Byte compile the python files on installation
ENV UV_COMPILE_BYTECODE=1
ENV UV_CACHE_DIR="/cache"
# Python version to use
ENV UV_PYTHON=python3.13
# Tweaking the PATH variable for easier use
ENV PATH="$UV_PROJECT_ENVIRONMENT/bin:$PATH"

########################################################################################################################
# `builder-base` stage is used to build deps + create our virtual environment
########################################################################################################################
FROM linux-base AS python-base

# Update debian
RUN apt-get update
RUN apt-get upgrade -y

# Would need libpq-dev us using psycopg2 and curl (& build-essential?)
# Other utils come in handy when inside a container especially during development
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    curl \
    dnsutils \
    git \
    iputils-ping \
    jq \
    libpq-dev \
    net-tools \
    telnet \
    wget \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Create virtual environment and install dependencies
COPY pyproject.toml uv.lock ./
COPY packages ./
RUN --mount=type=cache,target=$UV_CACHE_DIR uv sync --all-extras --frozen --no-dev --no-install-project

########################################################################################################################
# 'development' stage installs all dev deps and can be used to develop code.
# For example using docker-compose to mount local volume under /app
########################################################################################################################
FROM python-base AS development

# Install dev dependencies
RUN --mount=type=cache,target=$UV_CACHE_DIR uv sync --all-extras --frozen --no-install-project

# this will become the mount point of our code. (docker-compose)
WORKDIR /app

COPY ./docker/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./docker/local/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

EXPOSE 8000

ENTRYPOINT ["/entrypoint"]
CMD ["/start"]

########################################################################################################################
# Below Stages are for Production Builds
########################################################################################################################

# First we need to build the front end using Node & Vite
FROM node:22-bookworm-slim AS frontend-builder

WORKDIR /app

RUN echo "Installing dependencies"

COPY package.json package-lock.json vite.config.js ./
RUN npm ci && npm cache clean --force

# copy in the app source as we need all the templates and js files to build static assets
COPY . .

ENV NODE_ENV=production
RUN npm run build

########################################################################################################################
# Django Production
########################################################################################################################

FROM linux-base AS production

# Would need libpq-dev us using psycopg2 and curl (& build-essential?)
# Other utils come in handy when inside a container especially during development
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    curl \
    dnsutils \
    git \
    iputils-ping \
    jq \
    libpq-dev \
    net-tools \
    telnet \
    wget \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN addgroup --system django \
    && adduser --system --ingroup django django

WORKDIR /app

# Copy python, virtual env and static assets
COPY --chown=django:django --from=python-base $UV_PYTHON_INSTALL_DIR $UV_PYTHON_INSTALL_DIR
COPY --chown=django:django --from=python-base $UV_PROJECT_ENVIRONMENT $UV_PROJECT_ENVIRONMENT

# copy only the static assets built by vite from the frontend-builder
COPY --chown=django:django --from=frontend-builder /app/static ./static
# copy the contents of the src directory to the app directory
COPY --chown=django:django ./src ./

COPY --chown=django:django ./docker/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY --chown=django:django ./docker/production/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

# Switch to the non-root user
USER django

# Start the application server
EXPOSE 8000

ENTRYPOINT ["/entrypoint"]
CMD ["/start"]
