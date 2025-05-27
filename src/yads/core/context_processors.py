from typing import Any

from django.conf import settings
from django.http import HttpRequest

from config.settings.env import pydenset


def common(_: HttpRequest) -> dict[str, Any]:
    context = {
        'DEBUG': settings.DEBUG,
    }

    if settings.DEBUG:
        context['USE_VITE'] = pydenset.USE_VITE
        context['VITE_URL'] = pydenset.VITE_URL

    return context
