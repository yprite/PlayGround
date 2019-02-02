from .settings import *

#DEBUG MODE
DEBUG = True

ALLOWED_HOSTS = [
        '*',
]

for name, logger in LOGGING['loggers'].items():
    logger['level'] = 'INFO' if name == 'django' else 'DEBUG'
    logger['handlers'].append('console')

CRONTAB_DJANGO_MANAGE_PATH = os.path.join(BASE_DIR, 'stg-manage.py')
CRONJBOS = [] #Block crontab in Staging

