DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'data.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

#Email options:
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = '25'
EMAIL_HOST_USER = 'lakshman3@gmail.com'
EMAIL_HOST_PASSWORD = '123456'
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'admin@nikecup.in'
