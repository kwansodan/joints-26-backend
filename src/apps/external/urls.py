from django.urls import path


from .views.order_dispatch import *
from .views.order_payment import *

app_name = "external"

urlpatterns = [
    path(
        "order-payments/paystack/<str:pk>/",
        PaystackUpdateOrderPaymentDetailView.as_view(),
        name="paystack-update-order-payment",
    ),
    path(
        "order-dispatch/wegoo/<str:pk>/",
        WegooDispatchDetailView.as_view(),
        name="wegoo-dispatch-detail-view",
    ),
]
