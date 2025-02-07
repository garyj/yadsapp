import pytest
from django.templatetags.static import static as django_static

from yads.core.templatetags import core_tags


@pytest.fixture(autouse=True)
def reset_manifest():
    # Reset global manifest between tests
    yield
    with core_tags._manifest_lock:
        core_tags._manifest = None


def test_debug_mode_returns_vite_url_prefix(settings):
    settings.DEBUG = True
    settings.USE_VITE = True
    settings.VITE_URL = 'http://localhost:5173'
    settings.STATIC_ROOT = '/tmp'  # noqa: S108
    filename = '/app.js'
    result = core_tags.static(filename)
    expected = f'http://localhost:5173{django_static(filename.lstrip("/"))}'
    assert result == expected


def test_production_mode_returns_hashed_filename(settings):
    settings.DEBUG = False
    settings.STATIC_ROOT = '/tmp'  # noqa: S108
    settings.VITE_URL = 'http://localhost:5173'
    # Set a dummy manifest with a hashed file mapping.
    dummy_manifest = {'app.js': {'file': 'app.hash.js'}}
    with core_tags._manifest_lock:
        core_tags._manifest = dummy_manifest
    filename = '/app.js'
    result = core_tags.static(filename)
    expected = django_static('app.hash.js')
    assert result == expected
