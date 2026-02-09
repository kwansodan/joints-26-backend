import os
import dj_database_url
from pathlib import Path
from decouple import config
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("DJANGO_SECRET_KEY", cast=str)

DEBUG = config("DJANGO_DEBUG", cast=bool) 

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
    "drf_spectacular",

    "src.apps.users",
    "src.apps.bikers",
    "src.apps.orders",
    "src.apps.vendors",

    "src.apps.scripts",
    "src.apps.payments",
    "src.apps.external",
    "src.apps.notifications"
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
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

DB_CONNECTION_URL = config("DATABASE_URL", cast=str)

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

CONSOLE_EMAILING = config("CONSOLE_EMAILING", cast=bool)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' if CONSOLE_EMAILING else'django.core.mail.backends.smtp.EmailBackend'   
EMAIL_HOST = config("EMAIL_HOST", cast=str)
EMAIL_PORT = config("EMAIL_PORT", cast=str)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", cast=str)
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", cast=str)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool)
EMAIL_USE_SSL = config("EMAIL_USE_SSL", cast=bool)

ADMIN_USER_NAME = config("ADMIN_USER_NAME", cast=str, default="Admin User")
ADMIN_USER_EMAIL = config("ADMIN_USER_EMAIL", cast=str, default=None)

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
    "http://api.joints.com"
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

    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=10),
    "REFRESH_TOKEN_LIFETIME": timedelta(minutes=30),
}

AUTH_USER_MODEL = "users.User"

SPECTACULAR_SETTINGS = {
    'TITLE': 'Joints',
    'VERSION': '1.0.0', 
    'SERVE_INCLUDE_SCHEMA': False,
    'DESCRIPTION': 'Human assisted food ordering platform',
    'SERVERS': [
        {"url": "http://api.joints.com:8000", 
         "description": "joints backend api url"
        },
    ],
    'CONTACT': {
        "name": "dev-muftawu",
        "email": "mohammedyiwere@gmail.com",
    },
    'TAGS': [
        {"name": "auth", "description": "Authentication endpoints"},
        {"name": "users", "description": "User endpoints"},
        {"name": "vendors", "description": "Vendor endpoints"},
        {"name": "bikers", "description": "Biker endpoints"},
        {"name": "orders", "description": "Orders endpoints"},
        {"name": "payments", "description": "Payment endpoints"},
        {"name": "notifications", "description": "Notification endpoints"},
    ],
    'DEFAULT_CONTENT_TYPES': ['application/json'],
}

MNOTIFY_API_KEY = config("MNOTIFY_API_KEY", cast=str)

CELERY_BROKER_URL = config("CELERY_BROKER_URL", cast=str)
CELERY_RESULT_BACKEND = config("CELERY_RESULT_BACKEND", cast=str)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERY_ENABLE_UTC = True
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = config("CELERY_TASK_TIME_LIMIT", cast=int)

