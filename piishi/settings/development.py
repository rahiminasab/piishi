from piishi.settings.production import *

DEBUG = True
SECURE_SSL_REDIRECT = False

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "web/frontend/static")
]

MEDIA_ROOT = os.path.join('/home/ehsan/Desktop', 'media')