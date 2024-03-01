from django.urls import path
from .import views

# documentation with swagger
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='API Documentation')


urlpatterns = [

    # Objective
    
    # GET all
    path('objectives/', views.all_objectives, name='objectives_api'),
    # POST
    path('objectives/', views.create_objective, name='create_objective_api'),
    # GET id
    path('objectives/<int:objective_id>/',
         views.objective_detail, name='objective_detail'),
    # PUT
    path('objectives/<int:objective_id>/',
         views.update_objective, name='update_objective'),
    # DELETE
    path('delete_objective/<int:objective_id>/', views.delete_objective, name='delete_objective'),

    # get all the kpis of an objective and create one for this objective
    path('objectives/<int:objective_id>/kpis/', views.kpi_list_create, name='kpi_list_create'),
    # get all actions for an objective
    path('objectives/<int:objective_id>/actions/', views.action_objective, name='objective_actions_detail_api'),
     # list of questions for an objective
    path('objectives/<int:objective_id>/questions/', views.questions, name="action_questions"),


    # Action
    
    # GET all
    path('actions/', views.all_actions, name='actions_api'),
    # POST
    path('actions/', views.create_action, name='create_action'),
    # GET id
    path('actions/<int:id>/', views.action_details, name='actions_detail_api'),
    # PUT
    path('action/<int:id>/', views.update_action, name='update-action'),
    # DELETE
    path('actions/<int:id>/', views.delete_action, name='delete-action'),
    
    

    # teams
    # GET all
    path('teams/', views.all_teams, name='teams_api'),
    # POST
    path('teams/', views.create_team, name='team_create'),
    # GET id
    path('teams/<int:id>/', views.team_details, name='team_details'),
    # PUT
    path('teams/<int:id>/', views.update_team, name='update_team'),
    # DELETE
    path('delete-teams/<int:id>/', views.delete_team, name='delete_team'),
    
    # all users of a team
    path('teams/<int:id>/users/', views.team_users, name='team_users'),


    # User
    # GET all
    path('users/', views.all_users, name='all_users'),
    # GET id 
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
    # PUT
    path('users/<int:id>/', views.update_user, name='update_user'),
    # DELETE
    path('users/<int:id>/', views.delete_user, name='delete_user'),
    # POST
    path('users/', views.create_user, name='create_user'),
    
    # get all user in the same team as a user
     path('users/<int:user_id>/teams/',
         views.users_in_same_team, name='users_in_same_team'),



    # KPI
    # POST
    path('kpis/', views.create_kpi, name="create_kpi"),
    # GET all
    path('kpis/', views.kpis_all, name="kpis_all"),
    # GET id
    path('kpis/<int:id>/', views.kpi_details, name="kpis_all"),
    # PUT
    path('kpis/<int:id>/', views.update_kpi, name='update_kpi'),
    # DELETE
    path('kpis/<int:id>/', views.delete_kpi, name='delete_kpi'),


    # Tool
    # GET
    path('tools/', views.all_tools, name="all_tools"),
    # POST
    path('tools/', views.create_tool, name="create_tool"),
    # PUT
    path('tools/<int:tool_id>/', views.update_tool, name="update_tool"),
    # DELETE
    path('tools/<int:tool_id>/', views.delete_tool, name="delete_tool"),
    # GET id
    path('tools/<int:tool_id>/', views.tool_details, name="tool_details"),
    
    
    
    # Skill
    # GET all
    path('skills/', views.get_skills, name="skills"),
    # POST
    path('skills/', views.create_skill, name="skills"),
    # GET id
    path('skills/<int:skill_id>', views.skill_details, name="skill_details"),
    # PUT
    path('skills/<int:skill_id>', views.update_skill, name="update_skill"),
    # DELETE
    path('skills/<int:skill_id>',
         views.delete_skill, name="delete_skill"),
    
    
    # Task
    # GET all
    path('tasks/', views.get_all_tasks, name="tasks"),
    # POST
    path('tasks/', views.create_task, name="tasks"),
    # GET id
    path('tasks/<int:id>/', views.task_details, name='update-kpi'),
    # UPDATE
    path('tasks/<int:id>/', views.update_task, name='update-kpi'),
    # DELETE
    path('tasks/<int:id>/', views.delete_task, name='delete-kpi'),
    

    # Main Action Entry
    
     # GET  all
    path('action-main-entries/', views.action_main_entry_all, name='action_main_entry_all'),
    # GET id
    path('action-main-entries/<int:id>/', views.action_main_entry_details, name='action_main_entry_details'),
    
    # DELETE
    path('action-main-entries/<int:id>/', views.delete_action_main_entry, name='delete_action_main_entry'),
    # PUT
    path('action-main-entries/<int:id>/', views.action_main_entry_update, name='action_main_entry_update'),
    # POST
    path('action-main-entries/', views.create_action_main_entry, name='create_action_main_entry'),
    # GET: get actions for a particular date
    path('action-main-entries/<str:date>/', views.get_actions_for_date, name='get_actions_for_date'),
    # http://localhost:8000/action-main-entries/2023-01-01/
    
    # GET: actions entries in a timeframe
    path('action-main-entries/<str:start_date>/<str:end_date>/', views.get_actions_in_timeframe, name='get_actions_i_timeframe'),
    # YYYY-MM-DD
    
    # GET all: get all actions of an objective
    path('action-main-entries/<int:objective_id>/', views.action_main_entry_objective,
         name='action_main_entry_objective'),
   

    # Publish an objective
    path('objectives/publish_objective/<int:objective_id>/',
         views.publish_objective, name='publish_objective'),
    # list of published objectives
    path('objectives/published_objectives/', views.published_objectives,
         name='published_objectives'),
    # list of completed objectives
    path('objectives/completed_objectives/', views.completed_objectives,
         name='completed_objectives'),



    # Supervisor dashboard

    # Get op goals assigned to a aser and get all objectives related to those op goals
    path('objectives/objectives_assigned_to_user/<int:user_id>/',
         views.objectives_assigned_to_user, name='objectives_assigned_to_user'),
    # Get all completed objectives related to an operational goal
    path('objectives/completed_objectives_for_op_goal/<int:op_goal_id>/',
         views.completed_objectives_for_op_goal, name='completed_objectives_for_op_goal'),



    # Performance metrics

    # Objective Achievement Rate (OAR)
    path('objectives/user_performance/<int:user_id>/<str:start_date>/<str:end_date>/',
         views.user_performance, name='user_performance'),
    # e.g.  /api/user_performance/<user_id>/2024-01-01/2024-01-31/

    # Average Number of Actions per Objective (ANA/O)
    path('objectives/user_average_actions_objective/<int:user_id>/<str:start_date>/<str:end_date>/',
         views.average_actions_per_objective, name='user_average_actions_objective'),


]
