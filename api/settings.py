import os
import dj_database_url
from pathlib import Path
from decouple import config
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("djangoSecretKey", cast=str)

DEBUG = config("djangoDebug", cast=bool) 

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "api.joints.com"]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    "corsheaders",
    "rest_framework",

    "src.apps.menu",
    "src.apps.users",
    "src.apps.bikers",
    "src.apps.vendors",

    "src.apps.scripts",
    "src.apps.payments",
    "src.apps.notifications"
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'api.wsgi.application'

DB_CONNECTION_URL = config("databaseUrl", cast=str)

DATABASES = {
    'default': dj_database_url.parse(
        f"{DB_CONNECTION_URL}",
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'

MEDIA_URL = 'media/'

MEDIA_ROOT = os.path.join(BASE_DIR, "src/media/")

CONSOLE_EMAILING = config("consoleEmailing", cast=bool)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' if CONSOLE_EMAILING else'django.core.mail.backends.smtp.EmailBackend'   
EMAIL_HOST = config("emailHost", cast=str)
EMAIL_PORT = config("emailPort", cast=str)
EMAIL_HOST_USER = config("emailHostUser", cast=str)
EMAIL_HOST_PASSWORD = config("emailHostPassword", cast=str)
EMAIL_USE_TLS = config("emailUseTls", cast=bool)
EMAIL_USE_SSL = config("emailUseSsl", cast=bool)

ADMIN_USER_NAME = config("adminUserName", cast=str, default="Admin User")
ADMIN_USER_EMAIL = config("adminUserEmail", cast=str, default=None)

ADMINS = []
MANAGERS = []

if all([ADMIN_USER_NAME, ADMIN_USER_EMAIL]):
    ADMINS += [
        (f"{ADMIN_USER_NAME}", f"{ADMIN_USER_EMAIL}")
    ]
    MANAGERS = ADMINS


CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]


CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
)

CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],

    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

AUTH_USER_MODEL = "users.User"

