from .base_settings import *
from .deployment_settings import *
from .package_apps_settings import *
from .project_apps_settings import *
from .debug_settings import *
from .api_settings import *

if ENV == 'staging':
    from .environments.staging import *
elif ENV == 'production':
    from .environments.production import *
