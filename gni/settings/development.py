from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DEBUG_APPS = [
        'debug_toolbar',
]

INSTALLED_APPS += DEBUG_APPS
