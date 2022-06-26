from pathlib import Path
from dotenv import load_dotenv
from loguru import logger as loguru_logger
import os

# get data from .env
load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = bool(os.environ.get("DEBUG", default=0))

# ALLOWED_HOSTS = ["*"]
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # allauth
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # math in templates
    'mathfilters',

    # photo editor
    'sorl.thumbnail',

    # captcha
    'captcha',

    # debug tool bar
    "debug_toolbar",

    # apps
    'shop.apps.ShopConfig',
    'users',
    'cart',
]

SITE_ID = 1

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_MIN_LENGTH = 4
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 2

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # debug tool bar
    "debug_toolbar.middleware.DebugToolbarMiddleware",

    # 'bl_ishko.middleware.ErrorLogMiddleware',
]

ROOT_URLCONF = 'bl_ishko.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), os.path.join(BASE_DIR, 'templates', 'allauth')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'bl_ishko.context_processors.get_order',
                'bl_ishko.context_processors.get_categories',
                'bl_ishko.context_processors.get_new_products',
                'bl_ishko.context_processors.get_domain_name',
            ],
        },
    },
]

# allauth
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
ACCOUNT_EMAIL_SUBJECT_PREFIX = '[blishko.com] '

WSGI_APPLICATION = 'bl_ishko.wsgi.application'
LOGIN_REDIRECT_URL = 'shop:shop-page'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
# STATICFILES_DIRS = [BASE_DIR / "static"]


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
# EMAIL_USE_TLS = bool(int(os.getenv('EMAIL_USE_TLS')))
EMAIL_USE_SSL = bool(int(os.getenv('EMAIL_USE_SSL')))
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')

# Captcha
RECAPTCHA_PUBLIC_KEY = os.getenv('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = os.getenv('RECAPTCHA_PRIVATE_KEY')

# celery
# CELERY_BROKER_URL = 'amqp://localhost'
CELERY_BROKER_URL = 'redis://redis:6379'
CELERY_RESULT_BACKEND = 'redis://redis:6379'


# debug tool bar
INTERNAL_IPS = [
    "127.0.0.1",
]

# LOGURU
loguru_logger.add(os.path.join(BASE_DIR, 'logs/cart/logs.log'), format='{level} {time: HH:mm.ss DD.MM.YYYY} {name} ({function}) {message}', level='INFO', filter="cart.views", rotation='50 MB', compression='zip')
loguru_logger.add(os.path.join(BASE_DIR, 'logs/mails/logs.log'), format='{level} {time: HH:mm.ss DD.MM.YYYY} {name} ({function}) {message}', level='INFO', filter="cart.services", rotation='50 MB', compression='zip')
loguru_logger.add(os.path.join(BASE_DIR, 'logs/warning.log'), format='{level} {time: HH:mm.ss DD.MM.YYYY} {name} ({function}) {message}', level='WARNING', rotation='50 MB', compression='zip')
loguru_logger.add(os.path.join(BASE_DIR, 'logs/error.log'), format='{level} {time: HH:mm.ss DD.MM.YYYY} {name} ({function}) {message}', level='ERROR', rotation='50 MB', compression='zip')


# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://redis:6379',
    }
}
