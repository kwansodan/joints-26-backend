from .views import *
from django.urls import path 

app_name = "users"

urlpatterns = [  

    path("", 
         UserListView.as_view(),
         name="users-list-view"
    ),

    path("<str:pk>/",
         UserDetailView.as_view(),
         name="user-detail-view"
    )

]
