from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/interface/", 
         admin.site.urls
    ),

    path("auth/login/", 
         TokenObtainPairView.as_view(), 
         name="signin"
    ),

    path("auth/refresh/", 
         TokenRefreshView.as_view(), 
         name='token-refresh'
    ),

    path("users/",
        include("src.apps.users.urls")
    ),
]
