from typing import Any

from django.conf import settings
from django.http import HttpRequest


def common(_: HttpRequest) -> dict[str, Any]:
    return {
        'DEBUG': settings.DEBUG,
        'USE_VITE': settings.USE_VITE,
    }
