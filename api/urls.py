from django.urls import path
from .import views

urlpatterns = [
    # objectives
    path('', views.all_objectives, name='objectives_api'),
    path('create/', views.create_objective, name='create_objective_api'),  
    # get all the kpis of an objective and create one for this objectiive
    path('objective/<int:objective_id>/kpis/', views.kpi_list_create, name='kpi_list_create'),
    # details of an objective
    path('<int:objective_id>/', views.objective_detail, name='objective_detail'),
    
    

    # actions
    path('actions', views.all_actions, name='actions_api'),
    path('create_action/', views.create_action, name='create_action'),
    
    # teams
     path('teams', views.all_teams, name='teams_api'),
     path('teams/<int:id>/users/', views.team_users, name='team_users'),
    
    
    # users
    path('users/', views.all_users, name='all_users'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('users/<int:user_id>/same-team/', views.users_in_same_team, name='users_in_same_team'),
    
    # KPIs
    # create a kpi
    path('create_kpi', views.create_kpi, name="create_kpi"),
    # get the list of all kpis 
    path('kpis_all', views.kpis_all, name="kpis_all"),
    
]


