from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_objective, name='create_objective'),
]