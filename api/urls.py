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
    path('actions/<int:id>/', views.action_details, name='actions_detail_api'),
    path('actions_objective/<int:objective_id>/', views.action_objective, name='objective_actions_detail_api'),
    path('question/<int:objective_id>/', views.questions, name="action_questions"),
    
    # teams
    path('teams', views.all_teams, name='teams_api'),
    path('teams/<int:id>/users/', views.team_users, name='team_users'),
    path('teams/<int:pk>/', views.update_team, name='update_team'),
    path('delete-teams/<int:pk>/', views.delete_team, name='delete_team'),
    
    
    # users
    path('users/', views.all_users, name='all_users'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('users/<int:user_id>/same-team/', views.users_in_same_team, name='users_in_same_team'),
    path('update-users/<int:id>/', views.update_user, name='update_user'),
    path('delete-users/<int:id>/', views.delete_user, name='delete_user'),


    
    # KPIs
    # create a kpi
    path('create_kpi', views.create_kpi, name="create_kpi"),
    # get the list of all kpis 
    path('kpis_all', views.kpis_all, name="kpis_all"),
    # get tools
    path('all_tools', views.all_tools, name="all_tools"), 
    path('tool/<int:tool_id>/', views.update_tool, name="update_tool"),
    path('delete-tool/<int:tool_id>/', views.delete_tool, name="delete_tool"),
    # get skills
    path('skills', views.get_skills, name="skills"), 
    path('skills/<int:skill_id>', views.update_skill, name="update_skill"), 
    path('delete-skills/<int:skill_id>', views.delete_skill, name="delete_skill"),
    # get all tasks
    path('tasks', views.get_all_tasks, name="tasks"), 
    ]
