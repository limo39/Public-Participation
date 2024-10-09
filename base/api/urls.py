from django.urls import path
from . import views

urlpatterns = [
    path('',  views.getRoutes),
    path('bills/', views.getBills),
    path('bills/<str:pk>/', views.getBill),
]
