from .main import *


DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hatedetector',
        'USER': 'postgres',
        'PASSWORD': '2190',
        'CONN_MAX_AGE': 60,
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
'''

EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.zoho.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'noreply@swrdev.com.br'
EMAIL_HOST_PASSWORD = '@swrdev*'
