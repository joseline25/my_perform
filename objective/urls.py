from django.urls import path
from . import views

app_name = "objective"

urlpatterns = [
    path('', views.list_objective, name='list_objective'),
    path('create/', views.create_objective, name='create_objective'),
    path('details/<int:id>/', views.details_objective, name="detail_objective"),
    path('edit/<int:id>/', views.edit_objective, name="edit_objective"),
    
]