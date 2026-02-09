import os
from celery import Celery
from celery.signals import after_setup_task_logger

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')

app = Celery('api')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@after_setup_task_logger.connect
def setup_task_logger(logger, **kwargs):
    logger.info("Task logger is set up")
