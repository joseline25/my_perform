from django.contrib import admin
from .models import Team, Tool, Skill, TeamSkill, TeamTool, Objective, ObjectiveSkill, ObjectiveTool, KPI
from .models_additional.task import Task
# Register your models here.

# admin.site.register(Team)
admin.site.register(Tool)
admin.site.register(Skill)
admin.site.register(TeamSkill)
admin.site.register(TeamTool)
admin.site.register(Objective)
admin.site.register(ObjectiveSkill)
admin.site.register(ObjectiveTool)

admin.site.register(Task)

admin.site.register(KPI)

# this is to display the many to many fields of the model Team in  the admin side
class SkillInline(admin.TabularInline):  
    model = Team.skills.through
    
class UserInline(admin.TabularInline):  # or admin.StackedInline
    model = Team.users.through

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    inlines = [SkillInline, UserInline]
    list_display = ['name', 'description', 'created_at', 'created_by', 'updated_at']

