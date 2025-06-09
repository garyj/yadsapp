set export
set dotenv-load

sources := "src packages"

# default start docker compose in attached mode
_default:
    docker compose up

[private]
prereq:
    @uv --version || echo 'Please install UV: https://docs.astral.sh/uv/getting-started/installation/'
    @npm --version || echo 'Please install npm: https://docs.npmjs.com/downloading-and-installing-node-js-and-npm'
    @pre-commit --version || echo 'Please install pre-commit: `uv tool install pre-commit --with pre-commit-uv` or https://pre-commit.com/#install'

# Initialize the project with dependencies
bootstrap: prereq
    #!/usr/bin/env bash
    set -euo pipefail

    if [ ! -f ".env" ]; then
        cp .env.example .env
        echo ".env created"
    fi

    just install
    docker compose -f compose.yaml build --pull

# install all dependencies defined in pyproject.toml and package.json
install:
    uv sync --all-extras
    npm install

# upgrade/install all dependencies defined in pyproject.toml
upgrade:
    uv lock --upgrade
    npm upgrade

# bash shell into the running web container
bash:
    docker compose exec web bash

# run database migrations
migrate *ARGS:
    docker compose run --rm web python manage.py migrate {{ ARGS }}

# create database migrations
migrations *ARGS:
    docker compose run --rm web python manage.py makemigrations {{ ARGS }}

# start interactive shell
shell *ARGS:
    docker compose run --rm web python manage.py shell {{ ARGS }}

# start src/manage.py for all cases not covered by other commands
manage *ARGS:
    docker compose run --rm web python manage.py {{ ARGS }}

# destroy all docker-compose services and remove volumes and orphans
destroy:
    docker compose down -v --remove-orphans

# check code quality with ruff and npm linters
lint:
    uv run ruff check {{ sources }}
    uv run ruff format --check {{ sources }}
    npm run lint:standard
    npm run lint:prettier

# auto-fix code formatting with ruff and npm formatters
format:
    uv run ruff check --fix --unsafe-fixes {{ sources }}
    uv run ruff format {{ sources }}
    npm run format:standard
    npm run format:prettier

# run pre-commit rules on all files
pc:
    uv run --with pre-commit-uv pre-commit run --all-files

# run test suite
test *ARGS:
    uv run pytest {{ ARGS }}

# run test suite with coverage
coverage *ARGS:
    uv run pytest --cov --cov-report=html --cov-report=term {{ ARGS }}

# start docker-compose services
start:
    docker compose up -d

# build docker-compose services
build:
    docker compose up -d --build

# show logs of docker-compose services
logs:
    docker compose logs -f

# stop docker-compose services
stop:
    docker compose down

# restart docker-compose services
restart:
    docker compose restart

# rebuild and restart all docker-compose services
rebuild:  stop build start logs

# Create a superuser for the Django application
superuser:
	docker compose run -e DJANGO_SUPERUSER_PASSWORD=a --rm web \
	python manage.py createsuperuser --noinput \
	--username a --email="a@a.com.au"

########################################################################################################################
# Below targets use the compose-prod.yaml which tries to get closer to production
########################################################################################################################

# clean up production environment (remove volumes and orphans)
prodclean:
    docker compose -f compose-prod.yaml down -v --remove-orphans

# start production environment services in detached mode
prodstart:
    docker compose -f compose-prod.yaml up -d

# build and start production environment with forced recreation
prodbuild:
    docker compose -f compose-prod.yaml up -d --build --force-recreate

# follow logs from production environment services
prodlogs:
    docker compose -f compose-prod.yaml logs -f

# stop production environment services
prodstop:
    docker compose -f compose-prod.yaml down
