from .views.users import *
from django.urls import path 
from .views.auth_login import *

app_name = "users"

urlpatterns = [  

    path("", 
         UserListView.as_view(),
         name="users-list-view"
    ),

    path("detail/<str:pk>/",
         UserDetailView.as_view(),
         name="user-detail-view"
    )

]
