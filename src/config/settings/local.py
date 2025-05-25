from config.settings.base import *

# in local we use Whitenoise to server static files as we use uvicorn in development
sec_middleware_index = MIDDLEWARE.index('django.middleware.security.SecurityMiddleware')
MIDDLEWARE.insert(sec_middleware_index + 1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# STATIC
STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'pdj.utils.storages.LocalManifestStaticStorage'},
}


STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage',
    },
}
