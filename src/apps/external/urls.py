from django.urls import path

from .views.order_dispatch import *

app_name = "wegoo"

urlpatterns = [
    path(
        "order-dispatch/wegoo/<str:pk>/",
        WegooDispatchDetailView.as_view(),
        name="wegoo-dispatch-detail-view",
    )
]
