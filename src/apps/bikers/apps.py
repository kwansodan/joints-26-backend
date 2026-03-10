from django.apps import AppConfig

class BikersConfig(AppConfig):
    name = 'src.apps.bikers'

    def ready(self):
        import src.apps.bikers.signals
