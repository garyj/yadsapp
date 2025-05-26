# Django Project with Modern Frontend Stack

This is a modern Django project template featuring HTMX, Tailwind CSS, Alpine.js, and a comprehensive development setup.

## Technology Stack

- **Backend**: Django 5.2+, Python 3.13, PostgreSQL, HTMX
- **Frontend**: Vite, Tailwind CSS v4, Alpine.js, HTMX
- **Tools**: uv (dependency management), ruff (linting/formatting), pytest (testing), just (task runner)
- **Infrastructure**: Docker, Docker Compose

## Essential Commands (Just)

### Development

- `just` or `just _default`: Start development environment (docker compose up)
- `just start`: Start services in detached mode
- `just stop`: Stop all services
- `just restart`: Restart services
- `just build`: Build and start services
- `just rebuild`: Full rebuild (stop → build → start → logs)
- `just bash`: Shell into running web container
- `just logs`: Follow docker compose logs

### Django Management

- `just migrate [ARGS]`: Run database migrations
- `just migrations [ARGS]`: Create database migrations
- `just shell [ARGS]`: Django interactive shell
- `just manage [ARGS]`: Run any Django management command

### Code Quality

- `just lint`: Run all linters (ruff + npm linters)
- `just format`: Auto-format all code (ruff + npm formatters)
- `just pc`: Run pre-commit hooks on all files
- `just test [ARGS]`: Run test suite with pytest
- `just coverage [ARGS]`: Run tests with coverage report

### Dependencies

- `just upgrade`: Update all Python dependencies using uv

### Production

- `just prodstart`: Start production environment
- `just prodbuild`: Build production containers
- `just prodstop`: Stop production environment
- `just prodclean`: Clean production environment

## Project Structure

```bash
src/
├── config/               # Django configuration
│   ├── settings/         # Environment-specific settings
│   │   ├── base.py       # Base settings
│   │   ├── local.py      # Development settings
│   │   ├── production.py # Production settings
│   │   └── env.py        # Pydantic environment settings
│   ├── urls.py           # Root URL configuration
│   ├── wsgi.py           # WSGI application
│   └── asgi.py           # ASGI application
├── frontend/             # Frontend assets
│   ├── project.css       # Main CSS file (Tailwind)
│   └── project.js        # Main JS file (Alpine.js + HTMX)
├── templates/            # Django templates
│   └── base.html         # Base template
├── {{ project_name }}/                 # Django apps
│   └── core/             # Core app with custom User model
└── manage.py             # Django management script
```

## Code Style Guidelines

### Python

- **Linting**: Uses ruff with extensive rule set (see pyproject.toml)
- **Formatting**: Single quotes, 119 character line length
- **Type Hints**: Required for all function arguments and returns
- **Import Style**: Absolute imports required, no relative imports
- **Settings**: Use Pydantic for environment variables (see `src/config/settings/env.py`)

### Frontend

- **CSS**: Tailwind CSS v4 with `@import 'tailwindcss'`
- **JavaScript**: ES modules, Alpine.js for reactivity, HTMX for server interaction
- **Linting**: Standard.js + Prettier with specific plugins for Django templates

### Templates

- **Format**: Use django-template-partials for component-like templates
- **Icons**: Heroicons available via template tags

## Development Workflow

### Daily Development

1. **Start services**: `just start`
2. **Make changes**: Edit code (hot reload enabled)
3. **Run tests**: `just test` for specific tests, `just coverage` for full coverage
4. **Check code**: `just lint` before committing
5. **Format code**: `just format` to auto-fix formatting

### Creating New Features

1. **Models**: Add to appropriate app, then `just migrations` and `just migrate`
2. **Templates**: Place in `src/templates/`
3. **Static files**: Frontend assets go in `src/frontend/`, auto-compiled by Vite
4. **Tests**: Add to app's `tests/` directory, run with `just test`

## Environment Configuration

## Testing

### Running Tests

- `just test`: Run all tests
- `just test path/to/test.py`: Run specific test file
- `just test -k "test_name"`: Run tests matching pattern
- `just coverage`: Run with HTML coverage report

### Test Configuration

- **Framework**: pytest with django, mock, and coverage plugins
- **Settings**: Uses `config.settings.test` module
- **Database**: Separate test database created automatically

## Docker & Deployment

### Development

- Uses `docker/Dockerfile` with `development` target
- Hot reload enabled for Python and frontend files
- Database data persisted in `postgres_data` volume

### Production

- Multi-stage build: frontend build → Python build → final image
- Non-root user for security
- Static files built with Vite and served by WhiteNoise
- Uses `production` settings module

## Troubleshooting

### Common Issues

- **Port conflicts**: Check `APP_PORTS` and `DEBUG_PORTS` in `.env`
- **Database connection**: Ensure PostgreSQL container is running (`just logs`)
- **Static files**: Run `npm run build` if Vite assets aren't loading
- **Permissions**: Use `just bash` to debug container issues

### Performance

- **Database**: Check migrations with `just manage showmigrations`
- **Static files**: Vite dev server runs on port 5173 in development
- **Templates**: Cached in production, not in development

## Important Notes

- **Dependencies**: Always use `uv` for Python package management
- **Migrations**: Never edit existing migration files, create new ones
- **Static files**: Vite handles all frontend asset compilation
- **Settings**: Environment-specific settings in `config.settings/`
- **Security**: SECRET_KEY auto-generated in development, required in production
- **Database**: Uses custom User model in `yads.core.models.User`

## VS Code Integration

Recommended extensions:

- Python (with pyright for type checking)
- Ruff (for linting/formatting)
- Tailwind CSS IntelliSense
- Django (for template support)

## Custom Management Commands

Create management commands in `yads/core/management/commands/` following Django conventions.
