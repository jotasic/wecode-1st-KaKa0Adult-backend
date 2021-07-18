from .base   import *

SECRET_KEY = get_env_variable('DJANGO_SECRECT_KEY')
ALGORITHM = get_env_variable('DJANGO_ALGORITHM')

DEBUG      = False

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

LOG_FILE = os.path.join(BASE_DIR, 'log', 'application.log')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters':{
        'verbose' : {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S",
    },

    'simple' : {
        'format': '%(levelname)s %(message)s'
        },
    },

  'handlers': {

    'file': {
        'level': 'DEBUG',
        'class': 'logging.handlers.TimedRotatingFileHandler',
        'filename': LOG_FILE,
        'when': 'D',
        'interval': 1, 
        'backupCount': 10,
        'formatter': 'verbose',
        },
    },

    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}