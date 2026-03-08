import json

import redis
from django.conf import settings

REDIS_PUBSUB_HOST = settings.REDIS_PUBSUB_HOST
REDIS_PUBSUB_DB_INDEX = settings.REDIS_PUBSUB_DB_INDEX

rds = redis.Redis(host=REDIS_PUBSUB_HOST, port=6379, db=REDIS_PUBSUB_DB_INDEX)

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
