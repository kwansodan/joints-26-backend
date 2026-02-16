from .views.order import *
from .views.order_location import *
from django.urls import path 
from .views.order_item import *

app_name = "orders"

urlpatterns = [  

    # orders
    path("", 
         OrderListView.as_view(),
         name="order-list-view"
    ),

    path("detail/<str:pk>/",
         OrderDetailView.as_view(),
         name="order-detail-view"
    ),

    # order items
    path("orderitems/list/", 
         OrderItemListView.as_view(),
         name="orderitem-list-view"
    ),

    path("orderitems/detail/<str:pk>/",
         OrderItemDetailView.as_view(),
         name="orderitem-detail-view"
    ),

    # order location
    path("location/list/", 
         OrderLocationListView.as_view(),
         name="location-list-view"
    ),

    path("location/detail/<str:token>/<str:order_location_id>/",
         OrderLocationDetailView.as_view(),
         name="location-detail-view"
    ),
]
