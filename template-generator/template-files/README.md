
# YADS - Yet Another Django Starter

A personal and opinionated Django Starter that I use for new Django Projects.

Under the hood a combination of Django, Vite, Docker and has quite a nice developer experience with reasonably fast
builds, hot reloads on both template and Python files (controlled by Vite), VSCode config, and a number of useful `just`
recipes.

The template itself is generated automatically from [garyj/yadsapp](https://github.com/garyj/yadsapp). Github Actions
will push any changes made to [garyj/yadsapp](https://github.com/garyj/yadsapp) repo to this repo converting the project
to a template.

Commit messages used for commits to this template repo are entirely AI generated using Simon Willison
[llm](https://github.com/simonw/llm) tool.

Inspired by [jefftriplett/django-startproject](https://github.com/jefftriplett/django-startproject) and
[cookiecutter/cookiecutter-django](https://github.com/cookiecutter/cookiecutter-django).

## 🚩 Core Features

- Django 5.2+ with Python 3.13
- HTMX
- Tailwind CSS v4
- Alpine.js
- Docker & Docker Compose for development and production
- uv for fast Python package management

## 👕 Code Quality

- ruff for linting and formatting
- pytest for testing with coverage
- pre-commit hooks for code quality
- pyright for type checking
- prettier and standard for HTML and Javascript formatting using:
  - prettier-plugin-jinja-template which works "ok" with Django templates
  - prettier-plugin-organize-attributes for organizing HTML tag attributes

## 🛠️ Development Tools

- just for task automation
- Vite for frontend asset building
- Hot reload for Python and frontend files
- VS Code configuration included

## 📐 Vite Notes

I don't use any 3rd party Django package for Vite. Vite is used as per the [backend
integration](https://vite.dev/guide/backend-integration) docs.

There is also simple
[override](https://github.com/garyj/yads/blob/master/src/project_name/core/templatetags/core_tags.py) of the Django's
`static` tag that will simply prepent the Vite development URL in development. This is contolled via the [`USE_VITE`
setting](https://github.com/garyj/yads/blob/master/src/config/settings/env.py) which defaults to [`True` during
development](https://github.com/garyj/yads/blob/master/.env.example).

## Getting Started

```bash
# Create a new project
uv run --with=django django-admin startproject \
    --extension=ini,py,toml,yaml,yml,md,json \
    --template=https://github.com/garyj/yads/archive/main.zip \
    myproject

cd myproject

just bootstrap
```

## Usage

```bash
# Development
just                    # Start development environment (docker compose up)
just start              # Start services in detached mode
just stop               # Stop all services
just restart            # Restart services
just build              # Build and start services
just rebuild            # Full rebuild (stop → build → start → logs)
just bash               # Shell into running web container
just logs               # Follow docker compose logs

# Django Management
just migrate [ARGS]     # Run database migrations
just migrations [ARGS]  # Create database migrations
just shell [ARGS]       # Django interactive shell
just manage [ARGS]      # Run any Django management command

# Code Quality
just lint               # Run all linters (ruff + npm linters)
just format             # Auto-format all code
just test [ARGS]        # Run test suite with pytest
just coverage [ARGS]    # Run tests with coverage report
just pc                 # Run pre-commit hooks on all files

# Dependencies
just upgrade            # Update all Python & NPM dependencies

# Production
just prodbuild          # Build production containers
just prodstart          # Start production environment
just prodstop           # Stop production environment
just prodclean          # Clean production environment
```

## Requirements

- Python 3.13+
- Node.js 22+
- Docker and Docker Compose
- uv (Python package manager)
- just (task runner)

For comprehensive development guidance, see `CLAUDE.md`.

## License

MIT License
