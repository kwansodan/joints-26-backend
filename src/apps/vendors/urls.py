from .views.menu import *
from .views.vendor import *
from django.urls import path 

app_name = "vendors"

urlpatterns = [  

    path("", 
         VendorListView.as_view(),
         name="vendor-list-view"
    ),

    path("<str:pk>/",
         VendorDetailView.as_view(),
         name="vendor-detail-view"
    ),

    path("menu/list/", 
         MenuListView.as_view(),
         name="menu-list-view"
    ),

    path("menu/detail/<str:pk>/",
         MenuDetailView.as_view(),
         name="menu-detail-view"
    )

]
