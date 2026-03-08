from django.urls import path

from .views.serversent_events import *

app_name = "serversentevents"

urlpatterns = [
    path("", NotifyFrontendView.as_view(), name="notify-frontend-view"),
]
