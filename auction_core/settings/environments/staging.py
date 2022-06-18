import os

import dj_database_url

from auction_core.settings import TAG

ALLOWED_HOSTS = [f'{TAG}.{os.environ.get("ALLOWED_HOSTS")}']

DATABASES = {
    'default': dj_database_url.config()
}
