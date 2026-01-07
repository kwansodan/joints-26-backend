from . import views
from django.urls import path 

app_name = "vendors"

urlpatterns = [  

    path("", 
         views.vendorsView, 
         name="users-view"
    ),

    path("<str:pk>/",
         views.vendorDetailView,
         name="vendor-detail-view"
    ),
]
