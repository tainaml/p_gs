"""
Django settings for rede_gsti project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3u2oo))n_j*t#sjx*)=p*5j4mpb^7iruq4$v3%2nn!e2r2p$jj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Google Recaptcha keys
#
NORECAPTCHA_SITE_KEY = '6LccmgsTAAAAAGrsvn7r7aiIcnvbuIS7pyP0qv1K'
NORECAPTCHA_SECRET_KEY  = '6LccmgsTAAAAANyATh7UT3uL2G2iVnCCGfAXPE5f'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.mailmanager',
    'nocaptcha_recaptcha',
    'apps.account',
    'apps.article',
    'apps.comment',
    'apps.question',
    'apps.userprofile',
    'apps.socialaccount',
    'social.apps.django_app.default'


)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

ROOT_URLCONF = 'rede_gsti.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'rede_gsti.wsgi.application'

#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = 'apps.mailmanager.backend.MailManagedBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.mandrillapp.com'
EMAIL_HOST_USER = 'philliparente@gmail.com'
EMAIL_HOST_PASSWORD = 'gZ-tr-g2VKy6zQdRIVzmxg'
EMAIL_PORT = '587'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

#Comment config
ENTITY_TO_COMMENT = ['user', 'comment']
MAX_LEVELS = 2

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'sqlite': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'vagrant',
        'USER': 'vagrant',
        'PASSWORD': 'vagrant',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

#
LOGIN_URL = '/account/login'


# MailValidation Time
TIME_REGISTER_ACCOUNT = 48
TIME_RECOVERY_PASSWORD = 8

SITE_URL = 'http://localhost:8000'

SOCIAL_AUTH_FACEBOOK_KEY = '1486240068359213'
SOCIAL_AUTH_FACEBOOK_SECRET = 'd5be292ac55c13d465ae82bc19c84669'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '../../account/'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '810336189711-1m8lr2mdi9ci971e96440vsdve3g2r45.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'N6meHsg8fUGF4Ti4PKd0oh5m'
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['email']

AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    'social.backends.google.GoogleOAuth2',
    )

SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id, name, email'
}

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'apps.socialaccount.pipeline.require_email',
    'social.pipeline.mail.mail_validation',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.debug.debug',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
    'social.pipeline.debug.debug'
)