from django.urls import path
from . import views

urlpatterns = [
    path('action/create'),
    path('action/list'),
    path('action/view/<int:action_id>/'),
]
