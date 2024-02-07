from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_actions, name='list_actions'),
    path('create/', views.create_action, name='create_action'),
    path('details/<int:id>/', views.details_action, name="details_action"),
]
