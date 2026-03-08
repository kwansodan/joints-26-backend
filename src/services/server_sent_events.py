import json

import redis
from django.conf import settings

DJANGO_ENV = settings.DJANGO_ENV

R_HOST = "redis" if DJANGO_ENV == "prod" else "127.0.0.1"
R_DB_INDEX = 2

rds = redis.Redis(host=R_HOST, port=6379, db=R_DB_INDEX)

orderLocationUpdateChannel = "order_location_updates"


def notify_frontend(update_type, update_action, update_id, status):
    try:
        if update_type == "Order":

            match update_action:
                case "location":
                    rds.publish(
                        orderLocationUpdateChannel,
                        json.dumps(
                            {
                                "update_type": update_type,
                                "update_action": update_action,
                                "update_id": update_id,
                                "status": status,
                            }
                        ),
                    )

        else:
            pass
    except Exception as e:
        print("Failed to notify frontend", str(e))
