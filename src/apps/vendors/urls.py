from django.urls import path

from .views.menu import *
from .views.vendor import *
from .views.vendor_location import *

app_name = "vendors"

urlpatterns = [
    path("", VendorListView.as_view(), name="vendor-list-view"),
    path("detail/<str:pk>/", VendorDetailView.as_view(), name="vendor-detail-view"),
    path(
        "location/list/",
        VendorLocationListView.as_view(),
        name="vendor-location-list-view",
    ),
    path(
        "location/detail/<str:token>/<str:vendor_location_id>/",
        VendorLocationDetailView.as_view(),
        name="vendor-location-detail-view",
    ),
    path("menu/list/", MenuListView.as_view(), name="menu-list-view"),
    path("menu/detail/<str:pk>/", MenuDetailView.as_view(), name="menu-detail-view"),
]
