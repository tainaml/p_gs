from django.conf import settings
import defaults as app_settings

settings.configure(default_settings=app_settings, DEBUG=True)

