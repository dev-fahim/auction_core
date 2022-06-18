import os

import dj_database_url

ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOSTS')]
DEBUG = False

DATABASES = {
    'default': dj_database_url.config()
}
