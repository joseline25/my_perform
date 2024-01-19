from django.urls import path
from .import views

urlpatterns = [
    # objectives
    path('', views.all_objectives, name='objectives_api'),
    path('create/', views.create_objective, name='create_objective_api'),  
    path('<int:objective_id>/', views.objective_detail, name='objective_detail'),  

    # actions
    path('actions', views.all_actions, name='actions_api'),
    path('create_action/', views.create_action, name='create_action'),
    path('actions/<str:id>/', views.action_details, name='actions_detail_api'),
    path('actions/<str:id>/<str:objective_id>/', views.objectives_action, name='objective_actions_detail_api'),
    path('question/<str:objective_id>/', views.questions, name="action_questions"),
    
    # teams
     path('teams', views.all_teams, name='teams_api'),
     path('teams/<int:id>/users/', views.team_users, name='team_users'),
    
    
    # users
    path('users/', views.all_users, name='all_users'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('users/<int:user_id>/same-team/', views.users_in_same_team, name='users_in_same_team'),
    
]
