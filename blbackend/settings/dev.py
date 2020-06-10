from blbackend.settings.base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'blbackend',
        'USER': 'blbackend',
        'PASSWORD': 'blbackend',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
