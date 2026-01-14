from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path("admin/interface/", 
         admin.site.urls
    ),

    path("api/schema/", 
         SpectacularAPIView.as_view(), 
         name="schema"
    ),

    path("api/swagger-docs/", 
         SpectacularSwaggerView.as_view(url_name="schema"), 
         name="swagger-docs"),

    path("auth/login/", 
         TokenObtainPairView.as_view(), 
         name="signin"
    ),

    path("auth/refresh/", 
         TokenRefreshView.as_view(), 
         name='token-refresh'
    ),

    path("bikers/",
        include("src.apps.bikers.urls")
    ),

    path("users/",
        include("src.apps.users.urls")
    ),

    path("vendors/",
        include("src.apps.vendors.urls")
    ), 

    path("orders/",
        include("src.apps.orders.urls")
    ),

    path("payments/",
        include("src.apps.payments.urls")
    ),

    path("notifications/",
        include("src.apps.notifications.urls")
    ),
]
