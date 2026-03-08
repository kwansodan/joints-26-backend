from django.http import JsonResponse, StreamingHttpResponse
from django.views import View
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken

from src.services.server_sent_events import get_redis, orderLocationUpdateChannel


class NotifyFrontendView(View):

    @staticmethod
    def _event_stream():
        pubsub = get_redis().pubsub()
        pubsub.subscribe(orderLocationUpdateChannel)

        for message in pubsub.listen():
            if message["type"] == "message":
                print("received message", message)
                yield f"data: {message['data'].decode()}\n\n"
            else:
                yield ": keepalive\n\n"

    def get(self, request):
        token = request.GET.get("token")
        if not token:
            return JsonResponse({"message": "invalid token"}, status=401)
        try:
            AccessToken(token=token, verify=True)
        except TokenError:
            return JsonResponse({"message": "invalid token"}, status=401)

        response = StreamingHttpResponse(
            self._event_stream(), content_type="text/event-stream"
        )
        response["Cache-Control"] = "no-cache"
        response["X-Accel-Buffering"] = "no"
        return response
