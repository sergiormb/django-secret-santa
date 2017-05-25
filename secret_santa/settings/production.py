import os
from .base import *  # noqa

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = ['*']

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
# IMPORTANT!:
# You must keep this secret, you can store it in an
# environment variable and set it with:
# export SECRET_KEY="phil-dunphy98!-bananas12"
# https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/#secret-key
SECRET_KEY = os.environ['SECRET_KEY']

# WSGI SETTINGS
# https://docs.djangoproject.com/en/1.10/ref/settings/#wsgi-application
WSGI_APPLICATION = 'secret_santa.wsgi.application'

# SMTP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_HOST_USER = 'secretsantadjango@gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# NOTIFICATIONS
# A tuple that lists people who get code error notifications.
# https://docs.djangoproject.com/en/1.10/ref/settings/#admins
ADMINS = (
         ('Sergio', 'sergiormb88@gmail.com'),
)
MANAGERS = ADMINS

# DJANGO-COMPRESSOR SETTINGS
COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
)
STATICFILES_FINDERS = STATICFILES_FINDERS + (
    'compressor.finders.CompressorFinder',
)

enviroment = os.environ.get('ENVIRONMENT', '')
if enviroment:
    if enviroment == 'heroku':
        import dj_database_url
        db_from_env = dj_database_url.config(conn_max_age=500)
        DATABASES['default'].update(db_from_env)

        # Static files (CSS, JavaScript, Images)

        STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
        STATIC_URL = '/static/'

        # Extra places for collectstatic to find static files.
        STATICFILES_DIRS = [
            os.path.join(PROJECT_ROOT, 'secret_santa/static'),
        ]

        # Simplified static file serving.
        # https://warehouse.python.org/project/whitenoise/
        STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# Sentry

import raven

RAVEN_CONFIG = {
    'dsn': os.environ.get('DSN', ''),
}

try:
    from local_settings import * # noqa
except ImportError:
    pass
