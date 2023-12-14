from django.urls import path
from .views import ActionView


urlpatterns = [
    path('create/', ActionView.as_view(), name='create-action'),
]
