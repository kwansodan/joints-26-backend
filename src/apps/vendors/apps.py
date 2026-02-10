from django.apps import AppConfig

class VendorsConfig(AppConfig):
    name = 'src.apps.vendors'

    def ready(self):
        import src.apps.vendors.signals
