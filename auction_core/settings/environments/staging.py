import os

from auction_core.settings import TAG

ALLOWED_HOSTS = [f'{TAG}.{os.environ.get("ALLOWED_HOSTS")}']
