from piishi.settings.production import *

DEBUG = True

ALLOWED_HOSTS = ['*']
#SECURE_SSL_REDIRECT = False

# STATIC_ROOT = os.path.join(BASE_DIR, 'web/frontend/static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "web/frontend/static")
]

MEDIA_ROOT = os.path.join('/home/ehsan/Desktop', 'media')