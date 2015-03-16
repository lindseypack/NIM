"""
Django settings for network_inventory project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import re
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def _getSecretSettings():
    with open(os.path.join(BASE_DIR, "config")) as f:
        _config = f.read()
        _user = re.findall(r'DB_User = (.+?)\n', _config)[0].strip()
        _pw = re.findall(r'DB_Password = (.+?)\n', _config)[0].strip()
        _host = re.findall(r'DB_Host = (.+?)\n', _config)[0].strip()
        _secretKey = re.findall(r'DJ_SecretKey = (.+?)\n', _config)[0].strip()
        _allowedHosts = re.findall(r'DJ_Host = (.+?)\n', _config)
        return _secretKey, _allowedHosts, (_user, _pw, _host)

_secretKey, _allowedHosts, _DBInfo  = _getSecretSettings()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = _secretKey

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['*']
for host in _allowedHosts:
    ALLOWED_HOSTS.append(host.strip())

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'devices',
    'django_extensions',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'network_inventory.urls'

TEMPLATE_DIRS = (os.path.join(BASE_DIR, "templates"),)

WSGI_APPLICATION = 'network_inventory.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'network_inventory',
        'USER': _DBInfo[0],
        'PASSWORD': _DBInfo[1],
        'HOST': _DBInfo[2],
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_ROOT = (os.path.join(BASE_DIR, "static"))

STATIC_URL = '/static/'

TEMPLATE_DIRS = (os.path.join(BASE_DIR, "templates"),)


CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
