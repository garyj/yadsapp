import logging

from django import template
from django.conf import settings
from django.templatetags.static import static as django_static

from config.settings.env import pydenset

log = logging.getLogger(__name__)

register = template.Library()


@register.simple_tag
def static(filename: str) -> str:
    """Returns the URL of a static asset. Aware of Vite!

    In development mode with Debug enabled and USE_VITE set to ``True``, returns the URL from the Vite dev server.

    In production mode, simply delegates to Django's static file handling.

    Args:
        filename (str): The original filename of the static asset.

    Returns:
        str: The URL to the static asset.
    """
    if settings.DEBUG and pydenset.USE_VITE:
        return f'{pydenset.VITE_URL}{django_static(filename.lstrip("/"))}'

    return django_static(filename)
