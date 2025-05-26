
# YADS - Yet Another Django Starter

A personal Django Starter project that I use to get started quickly with new Django Apps.

This Django Template is auto generated from [garyj/yadsapp](https://github.com/garyj/yadsapp)

Inspired by [jefftriplett/django-startproject](https://github.com/jefftriplett/django-startproject)

## 🚩 Core Features

- Django 5.2+ with Python 3.13
- HTMX for seamless server-side interactions
- Tailwind CSS v4 for modern styling
- Alpine.js for lightweight reactivity
- Docker & Docker Compose for development and production
- uv for fast Python package management

## 👕 Code Quality

- ruff for linting and formatting
- pytest for testing with coverage
- pre-commit hooks for code quality
- pyright for type checking

## 🛠️ Development Tools

- just for task automation
- Vite for frontend asset building
- Hot reload for Python and frontend files
- VS Code configuration included

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
just logs               # Follow docker compose logs
just bash               # Shell into running web container

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
just upgrade            # Update all Python dependencies

# Production
just prodbuild          # Build production containers
just prodstart          # Start production environment
just prodstop           # Stop production environment
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
