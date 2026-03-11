import json

import redis
from django.conf import settings

DJANGO_ENV = settings.DJANGO_ENV
R_HOST = "redis" if DJANGO_ENV == "prod" else "127.0.0.1"
R_DB_INDEX = 2

_rds = None


def get_redis():
    global _rds
    if _rds is None:
        _rds = redis.Redis(host=R_HOST, port=6379, db=R_DB_INDEX)
    return _rds


orderUpdateChannel = "order_updates"


def notify_frontend(update_type, update_action, update_id, status):
    try:
        get_redis().publish(
            orderUpdateChannel,
            json.dumps(
                {
                    "update_type": update_type,
                    "update_action": update_action,
                    "update_id": update_id,
                    "status": status,
                }
            ),
        )
    except Exception as e:
        print("Failed to notify frontend", str(e))
