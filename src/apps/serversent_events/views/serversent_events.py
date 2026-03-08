import redis
from django.http import JsonResponse, StreamingHttpResponse
from django.views import View
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken

from src.services.server_sent_events import orderLocationUpdateChannel

rds = redis.Redis()


class NotifyFrontendView(View):

    @staticmethod
    def _event_stream():
        pubsub = rds.pubsub()
        pubsub.subscribe(orderLocationUpdateChannel)

        for message in pubsub.listen():
            if message["type"] == "message":
                yield f"data: {message['data'].decode()}\n\n"

    def get(self, request):
        token = request.GET.get("token")
        if not token:
            return JsonResponse({"message": "invalid token"}, status=401)
        try:
            AccessToken(token=token, verify=True)
        except TokenError:
            return JsonResponse({"message": "invalid token"}, status=401)
        return StreamingHttpResponse(
            self._event_stream(), content_type="text/event-stream"
        )
