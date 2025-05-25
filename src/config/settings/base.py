"""Django settings

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

import dj_database_url
import django_stubs_ext

from config.settings.env import pydenset

# Apply the monkey patches for django-stubs
# https://github.com/typeddjango/django-stubs?tab=readme-ov-file#i-cannot-use-queryset-or-manager-with-type-annotations
django_stubs_ext.monkeypatch()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# SECURITY WARNING: don't run with debug turned on in production!
# https://docs.djangoproject.com/en/5.1/ref/settings/#debug
DEBUG = pydenset.DEBUG
USE_VITE = pydenset.USE_VITE

# SECURITY WARNING: keep the secret key used in production secret!
# https://docs.djangoproject.com/en/5.1/ref/settings/#secret-key
SECRET_KEY = pydenset.SECRET_KEY or 'A_NOT_SO_SAVE_DEFAULT_KEY' if DEBUG else pydenset.SECRET_KEY

# A list of strings representing the host/domain names that this Django site can serve.
# https://docs.djangoproject.com/en/5.1/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [*pydenset.EXTRA_ALLOWED_HOSTS]

# A list of IP addresses that are allowed to access the django debug toolbar.
# https://docs.djangoproject.com/en/5.1/ref/settings/#internal-ips
INTERNAL_IPS = pydenset.INTERNAL_IPS

# A list of trusted origins for unsafe requests (e.g. POST).
# https://docs.djangoproject.com/en/5.1/ref/settings/#csrf-trusted-origins
CSRF_TRUSTED_ORIGINS = pydenset.CSRF_TRUSTED_ORIGINS

# Application definition
# https://docs.djangoproject.com/en/5.1/ref/settings/#installed-apps
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
]

# Third-party apps
THIRD_PARTY_APPS = [
    'django_htmx',
    'django_extensions',
    'template_partials.apps.SimpleAppConfig',
]

# Our apps
LOCAL_APPS = [
    'yads.core',
]

INSTALLED_APPS = [*DJANGO_APPS, *THIRD_PARTY_APPS, *LOCAL_APPS]

# Middleware definitions
# https://docs.djangoproject.com/en/5.1/topics/http/middleware/
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
]

# A string representing the full Python import path to your root URLconf.
# https://docs.djangoproject.com/en/5.1/ref/settings/#root-urlconf
ROOT_URLCONF = 'config.urls'


# used to disable the cache in dev, but turn it on in production.
# more here: https://nickjanetakis.com/blog/django-4-1-html-templates-are-cached-by-default-with-debug-true
default_loaders = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
]
cached_loaders = [('django.template.loaders.cached.Loader', default_loaders)]

production_loaders = [('template_partials.loader.Loader', cached_loaders)]
development_loaders = [('template_partials.loader.Loader', default_loaders)]

###

# A list containing the settings for all template engines to be used with Django.
# https://docs.djangoproject.com/en/5.1/ref/settings/#templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.csrf',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'yads.core.context_processors.common',
            ],
            'loaders': development_loaders if DEBUG else production_loaders,
            'builtins': [
                # "django.contrib.humanize.templatetags.humanize",
                'django.templatetags.i18n',
                # "django.templatetags.l10n",
                'django.templatetags.static',
                # "django.templatetags.tz"
                'heroicons.templatetags.heroicons',
            ],
        },
    },
]

# The full Python path of the WSGI application object that Django`s built-in servers
# (e.g. runserver) will use.
# https://docs.djangoproject.com/en/5.1/ref/settings/#wsgi-application
WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
DATABASES = {'default': dj_database_url.parse(pydenset.DATABASE_URL)}

# Authentication backends
# https://docs.djangoproject.com/en/5.1/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    'unique_user_email.backend.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_USER_MODEL = 'core.User'

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Password hashers
# https://docs.djangoproject.com/en/dev/topics/auth/passwords/
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.ScryptPasswordHasher',
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/
LANGUAGE_CODE = 'en'
TIME_ZONE = 'UTC'
USE_I18N = False
USE_TZ = True

# Static files (SCSS, CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
# https://docs.djangoproject.com/en/5.1/ref/settings/#static-files
STATIC_ROOT = BASE_DIR / 'static'
STATIC_URL = '/static/'
STATICFILES_DIRS = (str(BASE_DIR / 'static' / 'dist'),)


# User uploaded static files
# https://docs.djangoproject.com/en/5.1/ref/settings/#media-url
# https://docs.djangoproject.com/en/5.1/ref/settings/#media-root
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SILENCED_SYSTEM_CHECKS = [
    'staticfiles.W004',  # silence missing static files dir as we don't use it in development
]
