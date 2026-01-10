from .views.order import *
from .views.location import *
from django.urls import path 
from .views.order_item import *

app_name = "orders"

urlpatterns = [  

    # orders
    path("", 
         OrderListView.as_view(),
         name="order-list-view"
    ),

    path("<str:pk>/",
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

    # location
    path("location/list/", 
         LocationListView.as_view(),
         name="location-list-view"
    ),

    path("location/detail/<str:pk>/",
         LocationDetailView.as_view(),
         name="location-detail-view"
    ),
]
