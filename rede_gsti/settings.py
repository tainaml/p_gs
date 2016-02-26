"""
Django settings for rede_gsti project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of setti  ngs and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import ConfigParser

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Environment set
PROJECT_NAME = 'rede_gsti'
ENVIRONMENT_CONFIG_DIR = os.path.join(BASE_DIR, '%s/environment' % PROJECT_NAME)
ENVIRONMENT = os.environ.get(key="PROJECT_ENVIRONMENT", failobj="develop")

config = ConfigParser.RawConfigParser()
config_path = os.path.join(ENVIRONMENT_CONFIG_DIR, '%s-environment.cfg' % ENVIRONMENT)


try:
    config.readfp(open(config_path))
except IOError:
    config.add_section("GENERAL")
    config.set("GENERAL", "secret_key", '3u2oo))n_j*t#sjx*)=p*5j4mpb^7iruq4$v3%2nn!e2r2p$jj')
    config.set("GENERAL", "site_url", 'http://localhost:8000')
    config.set("GENERAL", "expiration_register_time", '48')
    config.set("GENERAL", "expiration_password_recovery", '8')

    config.add_section("STATIC")
    config.set("STATIC", "path", '/var/www/staticfiles/')
    config.set("STATIC", "path", '/var/www/staticfiles/')

    config.add_section("DATABASE")
    config.set("DATABASE", "name", "vagrant")
    config.set("DATABASE", "user", "vagrant")
    config.set("DATABASE", "password", "vagrant")
    config.set("DATABASE", "host", "db.redegsti.dev")
    config.set("DATABASE", "port", "5432")

    config.add_section("EMAIL")
    config.set("EMAIL", "tls", "true")
    config.set("EMAIL", "host", 'smtp.mandrillapp.com')
    config.set("EMAIL", "user", 'philliparente@gmail.com')
    config.set("EMAIL", "password", 'gZ-tr-g2VKy6zQdRIVzmxg')
    config.set("EMAIL", "port", '587')
    config.set("EMAIL", "from", 'philliparente@gmail.com')

    config.add_section("LOCALE")
    config.set("LOCALE", "code", 'pt-br')
    config.set("LOCALE", "timezone", 'America/Bahia')
    config.set("LOCALE", "i18n", 'true')
    config.set("LOCALE", "l10n", 'true')
    config.set("LOCALE", "tz", 'true')

    config.add_section("FACEBOOK")
    config.set("FACEBOOK", "key", '1486240068359213')
    config.set("FACEBOOK", "secret", 'd5be292ac55c13d465ae82bc19c84669')

    config.add_section("GOOGLE")
    config.set("GOOGLE", "key", '810336189711-1m8lr2mdi9ci971e96440vsdve3g2r45.apps.googleusercontent.com')
    config.set("GOOGLE", "secret", 'N6meHsg8fUGF4Ti4PKd0oh5m')

    config.add_section("THUMBOR")
    config.set("THUMBOR", "server", 'http://thumbor.redegsti.dev:8888')
    config.set("THUMBOR", "media_url", 'http://redegsti.dev:8000/media/uploads')
    config.set("THUMBOR", "key", 'MY_SECURE_KEY')

    config.add_section("CACHE")
    config.set("CACHE", "host", '127.0.0.1')
    config.set("CACHE", "port", '11211')

    config.add_section("LOG_FILES")
    config.set("LOG_FILES", "info", '/var/log/rede_gsti/info.log')
    config.set("LOG_FILES", "error", '/var/log/rede_gsti/error.log')
    config.set("LOG_FILES", "signals", '/var/log/rede_gsti/signals.log')

    config.add_section("GOOGLE_RECAPTCHA")
    config.set("GOOGLE_RECAPTCHA", "site_key", '6LccmgsTAAAAAGrsvn7r7aiIcnvbuIS7pyP0qv1K')
    config.set("GOOGLE_RECAPTCHA", "secret_key", '6LccmgsTAAAAANyATh7UT3uL2G2iVnCCGfAXPE5f')

    # with open(config_path, 'wb') as configfile:
    #     config.write(configfile)
    #     configfile.close()

print config.get("DATABASE", "name")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.get("GENERAL", "secret_key")

# SECURITY WARNING: don't run with debug turned on in production!

# DEBUG = True


# Vagrant Internal IP's
# INTERNAL_IPS = ('127.0.0.1', '10.0.2.2', '10.100.100.20', '10.100.100.15', '10.100.100.10')


# Google Recaptcha keys

NORECAPTCHA_SITE_KEY = '6LccmgsTAAAAAGrsvn7r7aiIcnvbuIS7pyP0qv1K'
NORECAPTCHA_SECRET_KEY = '6LccmgsTAAAAANyATh7UT3uL2G2iVnCCGfAXPE5f'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',

    # NINICO APP
    # 'apps.ninico',

    # PLUGINS
    'apps.mailmanager',
    'nocaptcha_recaptcha',
    'widget_tweaks',
    'django_thumbor',
    'autofixture',
    'django_migration_fixture',
    'celery',
    'djcelery',
    'social.apps.django_app.default',
    'ckeditor',
    'ckeditor_uploader',
    'django_user_agents',

    # CORE
    'apps.core',

    #Profiling
    #'debug_toolbar',

    # APPS
    'apps.account',
    'apps.geography',
    'apps.article',
    'apps.community',
    'apps.comment',
    'apps.userprofile',
    'apps.question',
    'apps.socialaccount',
    'apps.socialactions',
    'apps.taxonomy',
    'apps.contact',
    'apps.complaint',
    'apps.notifications',
    'apps.rede_gsti_signals',
    'apps.feed',
    'apps.configuration',
    'apps.custom_base'
)

### Setting Environment specific settings
if ENVIRONMENT == "develop":
    DEBUG = True
    INSTALLED_APPS += ('debug_toolbar','apps.ninico',)
elif ENVIRONMENT == "test":
    DEBUG = False
    ALLOWED_HOSTS = ['*']
elif ENVIRONMENT == "production":
    ALLOWED_HOSTS = ['*']
    DEBUG = False


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
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
                'django.core.context_processors.request'
            ],
        },
    },
]

WSGI_APPLICATION = '%s.wsgi.application' % PROJECT_NAME

# Populate file
FIXTURE_FILE = 'initial_data.json'


IMAGES_ALLOWED = ['image/jpeg','image/png']


# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = 'apps.mailmanager.backend.MailManagedBackend'
EMAIL_USE_TLS = config.getboolean("EMAIL", "tls")
EMAIL_HOST = config.get("EMAIL", "host")
EMAIL_HOST_USER = config.get("EMAIL", "user")
EMAIL_HOST_PASSWORD = config.get("EMAIL", "password")
EMAIL_PORT = config.getint("EMAIL", "port")
DEFAULT_FROM_EMAIL = config.get("EMAIL", "from")

# Comment config
ENTITY_TO_COMMENT = ['comment', 'article', 'answer']
MAX_LEVELS = 2

ENTITY_TO_COMPLAINT = ['article', 'question']

# Complaint config
COMPLAINT_COMMUNITY = 5

# Social config
SOCIAL_LIKE = 1
SOCIAL_UNLIKE = 2
SOCIAL_FOLLOW = 3
SOCIAL_FAVOURITE = 4
SOCIAL_SUGGEST = 5
SOCIAL_COMMENT = 6
SOCIAL_SEE_LATER = 7
SOCIAL_ANSWER = 8

SOCIAL_LABELS = {
    SOCIAL_LIKE: 'like',
    SOCIAL_UNLIKE: 'unlike',
    SOCIAL_FOLLOW: 'follow',
    SOCIAL_FAVOURITE: 'favourite',
    SOCIAL_SUGGEST: 'suggest',
    SOCIAL_COMMENT: 'comment',
    SOCIAL_SEE_LATER: 'see-later',
    SOCIAL_ANSWER: 'answer'
}

SOCIAL_ENTITIES = {
    SOCIAL_LIKE: ['comment', 'article', 'question', 'answer'],
    SOCIAL_UNLIKE: ['comment', 'article', 'question', 'answer'],
    SOCIAL_FOLLOW: ['community', 'user'],
    SOCIAL_FAVOURITE: ['article', 'question'],
    SOCIAL_SUGGEST: ['article', 'question'],
    SOCIAL_SEE_LATER: ['article', 'question'],
    SOCIAL_ANSWER: ['question']
}

SOCIAL_INVERSE_ACTIONS = {
    SOCIAL_LIKE: [SOCIAL_UNLIKE],
    SOCIAL_UNLIKE: [SOCIAL_LIKE],
    SOCIAL_FOLLOW: [],
    SOCIAL_FAVOURITE: []
}

TOOLBAR_CUSTOM = [
    ['Format'],
    ['Bold', 'Italic', 'Underline', 'Strike', '-', 'RemoveFormat'],
    ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
    ['NumberedList', 'BulletedList', '-', 'Blockquote'],
    ['Link', 'Unlink', 'Anchor'],
    ['Find'],
    ['HorizontalRule'],
    ['Image'],
    ['CodeSnippet'],
    ['Embed'],
    ['Maximize', 'ShowBlocks'],
    # ['Source']
]

# CKEDITOR
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Basic',
    },
    'question': {
        'toolbar': 'Custom',
        'toolbar_Custom': TOOLBAR_CUSTOM,
        'entities': False,
        'format_tags': 'h2;h3',
        'extraPlugins': ','.join([
            'autolink', 'autoembed', 'embedsemantic', 'widget',
            'dialog', 'embed', 'uploadimage',
            'codesnippet',
        ]),
    },
    'comment': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic'],
            ['CodeSnippet'],
        ],
        'entities': False,
        'extraPlugins': ','.join([
            'autolink', 'dialog',
            'codesnippet','autogrow','placeholder',
        ]),
    },
    'answer': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic'],
            ['CodeSnippet'],
        ],
        'entities': False,
        'extraPlugins': ','.join([
            'autolink', 'widget', 'dialog',
            'codesnippet',
        ]),
    },
    'article': {
        'toolbar': 'Custom',
        'toolbar_Custom': TOOLBAR_CUSTOM,
        'entities': False,
        'format_tags': 'h2;h3',
        'filebrowserBrowseUrl': None,
        'extraPlugins': ','.join([
            'autolink', 'autoembed', 'embedsemantic', 'widget',
            'dialog', 'embed', 'uploadimage',
            'codesnippet',
        ]),
    }
}

CKEDITORALLOW_NONIMAGE_FILES = False
CKEDITOR_RESTRICT_BY_USER = True
CKEDITOR_UPLOAD_PATH = 'editor-uploads/'
CKEDITOR_BROWSE_SHOW_DIRS = False


# NOTIFICATION
NOTIFICATION_LIKE = 1
NOTIFICATION_UNLIKE = 2
NOTIFICATION_FOLLOW = 3
NOTIFICATION_FAVOURITE = 4
NOTIFICATION_SUGGEST = 5
NOTIFICATION_COMMENT = 6
NOTIFICATION_SEE_LATER = 7
NOTIFICATION_ANSWER = 8

NOTIFICATION_ACTIONS = {

    NOTIFICATION_LIKE: 'like',
    NOTIFICATION_UNLIKE: 'unlike',
    NOTIFICATION_FOLLOW: 'follow',
    NOTIFICATION_FAVOURITE: 'favourite',
    NOTIFICATION_SUGGEST: 'suggest',
    NOTIFICATION_COMMENT: 'comment',
    NOTIFICATION_SEE_LATER: 'see-later',
    NOTIFICATION_ANSWER: 'answer'

}

NOTIFICATION_GROUP = {

    'members': [NOTIFICATION_FOLLOW],
    'general': [NOTIFICATION_LIKE, NOTIFICATION_UNLIKE],
    'posts': [NOTIFICATION_LIKE, NOTIFICATION_COMMENT, NOTIFICATION_ANSWER, NOTIFICATION_SUGGEST]

}

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'sqlite': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config.get("DATABASE", "name"),
        'USER': config.get("DATABASE", "user"),
        'PASSWORD': config.get("DATABASE", "password"),
        'HOST': config.get("DATABASE", "host"),
        'PORT': config.getint("DATABASE", "port"),
    },
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = config.get("LOCALE", "code")
TIME_ZONE = config.get("LOCALE", "timezone")
USE_I18N = config.getboolean("LOCALE", "i18n")
USE_L10N = config.getboolean("LOCALE", "l10n")
USE_TZ = config.getboolean("LOCALE", "tz")


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
STATIC_URL = '/static/'

# STATIC_ROOT = '/home/phillip/projects/python/django/rede_gsti/staticfiles/'
STATIC_ROOT = config.get("STATIC", "path")

# Media Paths: User upload files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media', 'uploads')
MEDIA_URL = '/media/uploads/'


# extramigrations
NASHVEGAS_MIGRATIONS_DIRECTORY = 'migrations/'


# THUMBOR
THUMBOR_SERVER = config.get("THUMBOR", "server")
THUMBOR_MEDIA_URL = config.get("THUMBOR", "media_url")
THUMBOR_SECURITY_KEY = config.get("THUMBOR", "key")
THUMBOR_ARGUMENTS = {}


# Login Urls
LOGIN_URL = '/account/login'


# Wizard Steps
WIZARD_STEPS_TOTAL = 3


# MailValidation Time
TIME_REGISTER_ACCOUNT = config.getint("GENERAL", "expiration_register_time")
TIME_RECOVERY_PASSWORD = config.getint("GENERAL", "expiration_password_recovery")

# Site Urls
SITE_URL = config.get("GENERAL", 'site_url')

SOCIAL_AUTH_FACEBOOK_KEY = config.get("FACEBOOK", "key")
SOCIAL_AUTH_FACEBOOK_SECRET = config.get("FACEBOOK", "secret")
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '../../account/'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config.get("GOOGLE", "key")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config.get("GOOGLE", "secret")
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
    'apps.socialaccount.pipeline.username_slugify',
    'apps.socialaccount.pipeline.validate_username',
    'social.pipeline.social_auth.associate_by_email',
    'social.pipeline.user.create_user',
    'apps.socialaccount.pipeline.create_profile',
    'apps.socialaccount.pipeline.save_profile_picture',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.debug.debug',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
    'social.pipeline.debug.debug'
)


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '%s:%s' % (config.get("CACHE", "host"), config.get("CACHE", "port"),),
    }
}


# Name of cache backend to cache user agents. If it not specified default
# cache alias will be used. Set to `None` to disable caching.
USER_AGENTS_CACHE = None


# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {

        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'info_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': config.get("LOG_FILES", "info")
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': config.get("LOG_FILES", "error")
        },
        'signal_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': config.get("LOG_FILES", "signals")
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
            # 'filters': ['special']
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins', 'error_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'general': {
            'handlers': ['console', 'info_file'],
            'level': 'INFO'
        },
        'signals': {
            'handlers': ['console', 'signal_file'],
            'level': 'INFO'
        }
    }
}