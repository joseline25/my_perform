from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_objective, name='list_objective'),
    path('create/', views.create_objective, name='create_objective'),
    
]