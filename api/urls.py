from django.urls import path
from .import views

# documentation with swagger
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='API Documentation')


urlpatterns = [
     
     # objectives
     path('', views.all_objectives, name='objectives_api'),
     path('create/', views.create_objective, name='create_objective_api'),
     # get all the kpis of an objective and create one for this objectiive
     path('objective/<int:objective_id>/kpis/',
          views.kpi_list_create, name='kpi_list_create'),
     # details of an objective
     path('<int:objective_id>/', views.objective_detail, name='objective_detail'),
     # update an objective
      path('update_objective/<int:objective_id>/', views.update_objective, name='update_objective'),
     # delete an objective
     path('delete_objective/<int:objective_id>/', views.delete_objective, name='delete_objective'),


     # actions
     path('actions', views.all_actions, name='actions_api'),
     path('create_action/', views.create_action, name='create_action'),
     path('actions/<int:id>/', views.action_details, name='actions_detail_api'),
     path('actions_objective/<int:objective_id>/',
          views.action_objective, name='objective_actions_detail_api'),
     path('question/<int:objective_id>/',
          views.questions, name="action_questions"),
     # update action
     path('update-action/<int:pk>/', views.update_action, name='update-action'),
     # delete action
     path('delete-action/<int:pk>/', views.delete_action, name='delete-action'),

     # teams
     path('teams', views.all_teams, name='teams_api'),
     path('teams/<int:id>/users/', views.team_users, name='team_users'),
     path('teams/<int:pk>/', views.update_team, name='update_team'),
     path('delete-teams/<int:pk>/', views.delete_team, name='delete_team'),


     # users
     path('users/', views.all_users, name='all_users'),
     path('users/<int:user_id>/', views.user_detail, name='user_detail'),
     path('users/<int:user_id>/same-team/',
          views.users_in_same_team, name='users_in_same_team'),
     path('update-users/<int:id>/', views.update_user, name='update_user'),
     path('delete-users/<int:id>/', views.delete_user, name='delete_user'),
     path('create_user/', views.create_user, name='create_user'),



     # KPIs
     # create a kpi and get details of a kpi
     path('create_kpi', views.create_kpi, name="create_kpi"),
     # get the list of all kpis
     path('kpis_all', views.kpis_all, name="kpis_all"),
     
     # update a kpi
      path('update_kpi/<int:pk>/', views.update_kpi, name='update_kpi'),
     # delete a kpi
     path('update_kpi/<int:pk>/', views.update_kpi, name='update_kpi'),
     
     
     # get tools
     path('all_tools', views.all_tools, name="all_tools"),
     path('tool/<int:tool_id>/', views.update_tool, name="update_tool"),
     path('delete-tool/<int:tool_id>/', views.delete_tool, name="delete_tool"),
     # get skills
     path('skills', views.get_skills, name="skills"),
     path('skills/<int:skill_id>', views.update_skill, name="update_skill"),
     path('delete-skills/<int:skill_id>',
          views.delete_skill, name="delete_skill"),
     # get all tasks
     path('tasks', views.get_all_tasks, name="tasks"),
     # update kpi
     path('update-kpi/<int:pk>/', views.update_kpi, name='update-kpi'),
     # delete kpi
     path('delete-kpi/<int:pk>/', views.delete_kpi, name='delete-kpi'),

     # Main Action Entry
     # create
     path('create_action_main_entry/', views.create_action_main_entry,
          name='create_action_main_entry'),
     # get actions for a particular date
     path('actions/<str:date>/', views.get_actions_for_date,
          name='get_actions_for_date'),
     # http://localhost:8000/actions/2023-01-01/
     # actions entries in a timeframe
     path('actions/<str:start_date>/<str:end_date>/',
          views.get_actions_in_timeframe, name='get_actions_i_timeframe'),
     # YYYY-MM-DD
     # get all actions of an objective
     path('action_main_entry_objective/<int:objective_id>/', views.action_main_entry_objective,
          name='action_main_entry_objective'),
     # get all the actions
     path('action_main_entry_all/', views.action_main_entry_all, name='action_main_entry_all'),

     # Publish an objective
     path('publish_objective/<int:objective_id>/', views.publish_objective, name='publish_objective'),
     # list of published objectives
     path('published_objectives/', views.published_objectives, name='published_objectives'),
     # list of completed objectives
     path('completed_objectives/', views.completed_objectives, name='completed_objectives'),

     # Performance metrics

     # Objective Achievement Rate (OAR)
     path('api/user_performance/<int:user_id>/<str:start_date>/<str:end_date>/',
          views.user_performance, name='user_performance'),
     # e.g.  /api/user_performance/<user_id>/2024-01-01/2024-01-31/

     # Average Number of Actions per Objective (ANA/O)
     path('api/user_average_actions_objective/<int:user_id>/<str:start_date>/<str:end_date>/',
          views.average_actions_per_objective, name='user_average_actions_objective'),


]
