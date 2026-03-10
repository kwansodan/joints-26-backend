from django.urls import path

from .views.biker import *
from .views.vehicle import *
from .views.delivery import *

app_name = "bikers"

urlpatterns = [  

    path("", 
         BikerListView.as_view(),
         name="bikers-list-view"
    ),

    path("detail/<str:pk>/",
         BikerDetailView.as_view(),
         name="biker-detail-view"
    ),

    path("vehicles/list/", 
         VehicleListView.as_view(),
         name="vehicle-list-view"
    ),

    path("vehicles/detail/<str:pk>/",
         VehicleDetailView.as_view(),
         name="vehicle-detail-view"
    ),

    path("order-deliveries/list/", 
         DeliveryListView.as_view(),
         name="delivery-list-view"
    ),

    path("order-deliveries/detail/<str:pk>/",
         DeliveryDetailView.as_view(),
         name="delivery-detail-view"
    )

]
