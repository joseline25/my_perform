from django.urls import path
from . import views
from .views import ActionView


urlpatterns = [
    path('', views.list_actions, name='list_actions'),
    #path('create/', views.create_objective, name='create_objective'),
    path('details/<int:id>/', views.details_action, name="details_action"),
]
