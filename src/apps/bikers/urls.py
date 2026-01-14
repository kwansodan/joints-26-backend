from .views.biker import *
from .views.vehicle import *
from django.urls import path 

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
    )

]
