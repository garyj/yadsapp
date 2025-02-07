set export
set dotenv-load

sources := "src packages"

# default start docker compose in attached mode
@_default:
    docker compose up

[private]
@check_uv:
    if ! command -v uv &> /dev/null; then \
        echo "uv could not be found. Exiting."; \
        exit; \
    fi

# upgrade/install all dependencies defined in pyproject.toml
@upgrade: check_uv
    uv sync --upgrade --all-extras

# bash shell into the running web container
@bash:
    docker compose exec web bash

# run database migrations
@migrate *ARGS: check_uv
    docker compose run --rm web python manage.py migrate {{ ARGS }}

# create database migrations
@migrations *ARGS: check_uv
    docker compose run --rm web python manage.py makemigrations {{ ARGS }}

# start interactive shell
@shell *ARGS: check_uv
    docker compose run --rm web python manage.py shell {{ ARGS }}

# start src/manage.py for all cases not covered by other commands
@manage *ARGS: check_uv
    docker compose run --rm web python manage.py {{ ARGS }}

@lint: check_uv
    uv run ruff check {{ sources }}
    uv run ruff format --check {{ sources }}
    npm run lint:standard
    npm run lint:prettier

@format: check_uv
    uv run ruff check --fix --unsafe-fixes {{ sources }}
    uv run ruff format {{ sources }}
    npm run format:standard
    npm run format:prettier

# run pre-commit rules on all files
@pc: check_uv
    uv run --with pre-commit-uv pre-commit run --all-files

# run test suite
@test *ARGS: check_uv
    uv run pytest {{ ARGS }}

# run test suite with coverage
@coverage *ARGS: check_uv
    uv run pytest --cov --cov-report=html --cov-report=term {{ ARGS }}

# start docker-compose services
@start:
    docker compose up -d

# build docker-compose services
@build:
    docker compose up -d --build

# show logs of docker-compose services
@logs:
    docker compose logs -f

# stop docker-compose services
@stop:
    docker compose down

# restart docker-compose services
@restart:
    docker compose restart

# rebuilds and starts docker-compose services
@rebuild: check_uv stop build start logs


########################################################################################################################
# Below targets use the compose-prod.yaml which tries to get closer to production
########################################################################################################################

@prodclean:
    docker compose -f compose-prod.yaml down -v --remove-orphans

@prodstart:
    docker compose -f compose-prod.yaml up -d

@prodbuild:
    docker compose -f compose-prod.yaml up -d --build --force-recreate

@prodlogs:
    docker compose -f compose-prod.yaml logs -f

@prodstop:
    docker compose -f compose-prod.yaml down
