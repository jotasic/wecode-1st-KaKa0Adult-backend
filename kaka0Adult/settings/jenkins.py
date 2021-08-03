from .base   import *

SECRET_KEY = get_env_variable('DJANGO_SECRECT_KEY')
ALGORITHM = get_env_variable('DJANGO_ALGORITHM')
DEBUG      = True

DATABASES = {
    'default' : {
        'ENGINE': get_env_variable('SQL_ENGINE'),
        'NAME': get_env_variable('SQL_DATABASE'),
        'USER': get_env_variable('SQL_USER'),
        'PASSWORD': get_env_variable('SQL_PASSWORD'),
        'HOST':  get_env_variable('SQL_HOST'),
        'PORT': get_env_variable('SQL_PORT'),
        'OPTIONS' : {
            'charset' : 'utf8mb4'
        }
    }
}