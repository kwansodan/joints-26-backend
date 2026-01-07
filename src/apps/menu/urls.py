from . import views
from django.urls import path 

app_name = "menu"

urlpatterns = [  

    path("", 
         views.menuView, 
         name="menu-view"
    ),

    path("<str:pk>/",
         views.menuDetailView,
         name="menu-detail-view"
    ),
]
