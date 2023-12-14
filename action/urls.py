from django.urls import path
from . import views
from .views import ActionView


urlpatterns = [
    path('action/create'),
    path('action/list'),
    path('action/view/<int:action_id>/'),
    path('create/', ActionView.as_view(), name='create-action'),

]
