from django.urls import path 
from .views.notification import *

app_name = "notifications"

urlpatterns = [  

    # orders
    path("", 
         NotificationListView.as_view(),
         name="notification-list-view"
    ),

    path("detail/<str:pk>/",
         NotificationDetailView.as_view(),
         name="notification-detail-view"
    ),
]

# gunicorn --bind 0.0.0.0:8000 --worker-class gevent --workers 6 --timeout 0 --log-level debug api.wsgi

