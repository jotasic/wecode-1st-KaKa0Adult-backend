from .base   import *

SECRET_KEY = get_env_variable('DJANGO_SECRECT_KEY')
ALGORITHM = get_env_variable('DJANGO_ALGORITHM')

TEST_RUNNER = 'kaka0Adult.test_runner.TestNoDBRunner'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}