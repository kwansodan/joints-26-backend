from .views.payment import *
from django.urls import path 

app_name = "payments"

urlpatterns = [  

    # orders
    path("", 
         PaymentListView.as_view(),
         name="payment-list-view"
    ),

    path("<str:pk>/",
         PaymentDetailView.as_view(),
         name="payment-detail-view"
    ),
]
