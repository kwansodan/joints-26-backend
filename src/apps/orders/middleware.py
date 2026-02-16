from django.http import HttpResponse
from django.shortcuts import redirect


class OrderLocationCaptureMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        print("request path", request.path)

        return response
