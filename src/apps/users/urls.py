from django.urls import path

from .views.auth_login import *
from .views.customers import *
from .views.users import *

app_name = "users"

urlpatterns = [
    path("", UserListView.as_view(), name="users-list-view"),
    path("detail/<str:pk>/", UserDetailView.as_view(), name="user-detail-view"),
    path("customers/", CustomerListView.as_view(), name="customer-list-view"),
    path(
        "customer/detail/<str:pk>/",
        CustomerDetailView.as_view(),
        name="customer-detail-view",
    ),
]
