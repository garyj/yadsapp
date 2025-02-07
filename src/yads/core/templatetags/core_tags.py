import json
import logging
from pathlib import Path
from threading import Lock

from django import template
from django.conf import settings
from django.templatetags.static import static as django_static

log = logging.getLogger(__name__)

register = template.Library()


_manifest = None
_manifest_lock = Lock()


def _get_manifest() -> dict:
    global _manifest  # noqa: PLW0603
    if _manifest is not None:
        return _manifest

    with _manifest_lock:
        if _manifest is None:
            manifest_path = Path(settings.STATIC_ROOT) / 'dist' / '.vite' / 'manifest.json'
            try:
                with manifest_path.open(encoding='utf-8') as f:
                    _manifest = json.load(f)
            except (OSError, json.JSONDecodeError):
                log.exception('Manifest not found or invalid')
                _manifest = {}

    return _manifest


@register.simple_tag
def static(filename: str) -> str:
    """
    Returns the URL of a static asset, aware of Vite.

    In development mode with Debug enabled, returns the URL from the Vite dev server.
    In production mode, uses the manifest to get the hashed asset filename.

    Args:
        filename (str): The original filename of the static asset.

    Returns:
        str: The URL to the static asset.
    """
    if settings.DEBUG and settings.USE_VITE:
        # Development mode with Vite dev server
        vite_url = getattr(settings, 'VITE_URL', 'http://localhost:5173')
        return f'{vite_url}{django_static(filename.lstrip("/"))}'

    # Production mode, use the manifest
    manifest = _get_manifest()
    if not manifest:
        # Manifest not available, fall back to static()
        return django_static(filename)
    # Ensure the filename is correctly formatted
    key = filename.lstrip('/')
    asset = manifest.get(key)
    if not asset:
        # Asset not found in manifest, fall back to static()
        return django_static(filename)
    # Get the hashed filename from the manifest
    hashed_filename = asset['file']
    return django_static(hashed_filename)
