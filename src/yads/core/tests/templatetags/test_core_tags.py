import pytest
from django.templatetags.static import static as django_static

from yads.core.templatetags import core_tags


@pytest.fixture
def enable_vite():
    from config.settings.env import pydenset

    vite_settings_backup = pydenset.USE_VITE
    pydenset.USE_VITE = True
    yield
    pydenset.USE_VITE = vite_settings_backup


@pytest.mark.usefixtures('enable_vite')
def test_debug_mode_returns_vite_url_prefix(settings):
    settings.DEBUG = True
    settings.VITE_URL = 'http://localhost:5173'
    settings.STATIC_ROOT = '/tmp'  # noqa: S108
    filename = '/app.js'
    result = core_tags.static(filename)
    expected = f'http://localhost:5173{django_static(filename.lstrip("/"))}'
    assert result == expected


def test_production_mode_returns_hashed_filename(settings):
    settings.DEBUG = False
    settings.VITE_URL = 'http://localhost:5173'
    filename = '/app.js'
    result = core_tags.static(filename)
    expected = django_static('app.js')
    assert result == expected
