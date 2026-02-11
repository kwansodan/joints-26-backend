from .views.wegoo import *
from django.urls import path 

app_name = "wegoo"

urlpatterns = [  

    path("wegoo/dispatch/<str:pk>/",
         WegooDispatchDetailView.as_view(),
         name="wegoo-dispatch-detail-view"
    )

]
