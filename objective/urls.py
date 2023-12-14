from django.urls import path
from . import views

app_name = "objective"

urlpatterns = [
    path('', views.list_objective, name='list_objective'),
    path('create/', views.create_objective, name='create_objective'),
    path('details/<int:objective_id>/', views.details_objective, name="detail_objective"),
    path('edit/<int:id>/', views.edit_objective, name="edit_objective"),
    path('edit_kpi/<int:id>/<int:objective_id>', views.edit_kpi, name="edit_kpi"),
    path('details_kpi/<int:id>',views.details_kpi, name='detail_kpi'),
    
    # corrections after the demo of december 12th
    path('create_two/', views.create_objective_two, name= 'create_objective_two'),
    
]