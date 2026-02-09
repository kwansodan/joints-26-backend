from django.apps import AppConfig

class NotificationsConfig(AppConfig):
    name = 'src.apps.notifications'

    def ready(self):
        import src.apps.notifications.signals
