from . import views
from django.urls import path 

app_name = "users"

urlpatterns = [  

    path("", 
         views.usersView, 
         name="users-view"
    ),

    path("<str:pk>/",
         views.userDetailView,
         name="user-detail-view"
    ),
    
    # path("user-update-password", 
    #      views.updatePasswordView, 
    #      name="user-update-password"
    # ),
    #
]
