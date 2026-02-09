from django.apps import AppConfig

class OrdersConfig(AppConfig):
    name = 'src.apps.orders'

    def ready(self):
        import src.apps.orders.signals
