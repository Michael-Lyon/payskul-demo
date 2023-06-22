"""
Django settings for payskul project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import datetime
import dj_database_url
from dotenv import load_dotenv
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


load_dotenv(os.path.join(BASE_DIR, ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # internal apps
    'account',
    'core',
    'book_store',
    'apiv1',
    # "okra_things",
    
    # packages
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'django_celery_beat', 
]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "payskul.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "payskul.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases



# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

DATABASE_URL = os.getenv("DATABAE_URL")
ENV = os.getenv("ENV")
# Extra lookup directories for collectstatic to find static files
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

HASHID_FIELD_SALT ="1*pjfyurp74dkt(3@4roi  # b@e_@l%!1vhj4xvv*f_jkapjm1!z"
HASHID_FIELD_ALLOW_INT_LOOKUP = True
HASHID_FIELD_ENABLE_HASHID_OBJECT = False


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
if ENV == "LOCAL":
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
ADMIN_USER = "pygod.dev@mail.com"
EMAIL_HOST = 'mail.payskul.com'
EMAIL_PORT = 465
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'mail@payskul.com'
EMAIL_HOST_PASSWORD = 'Simple@12'

ONLINE = True
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # "rest_framework.authentication.SessionAuthentication",
        "apiv1.authentication.TokenAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    # TODO: REMOVE THIS AND ADD CSRF BACK
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PERMISSION_CLASSES ': [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ], 
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 3,
}

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]



secret = os.getenv("OKRA_SECRET")
API_KEY = os.getenv("OKRA_PUBLIC")



SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# https://lanceproject-production-0863.up.railway.app/
# CSRF_TRUSTED_ORIGINS = ["*"]


CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.getenv("CELERY_BROKER_URL")
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_WORKER_PREFETCH_MULTIPLIER = 1
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True




if ENV == "LOCAL":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASE_URL = os.getenv("DATABASE_URL")

    DATABASES = {
        "default": dj_database_url.config(default=DATABASE_URL, conn_max_age=1800),
    }


SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ["Bearer"],
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(hours=10000),
    "REFRESH_TOKEN_LIFETIME": datetime.timedelta(hours=10000)
}


OKRA_PUBLIC = os.getenv("OKRA_PUBLIC")
OKRA_SECRET = os.getenv("OKRA_SECRET")


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'warning.log',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'okra_validator': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django': {
            'handlers': ['file', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
