__author__ = 'phillip'

from django.apps import AppConfig


class RedeGSTIConfig(AppConfig):
    name = 'apps.rede_gsti_signals'
    verbose_name = "RedeGSTISignals"

    def ready(self):
        pass
