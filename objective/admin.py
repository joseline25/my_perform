from django.contrib import admin
from .models import Team, Tool, Skill, TeamSkill, TeamTool, Objective, ObjectiveSkill, ObjectiveTool, DefinitionOfGood
from .models_additional.task import Task, Achievement
# Register your models here.

admin.site.register(Team)
admin.site.register(Tool)
admin.site.register(Skill)
admin.site.register(TeamSkill)
admin.site.register(TeamTool)
admin.site.register(Objective)
admin.site.register(ObjectiveSkill)
admin.site.register(ObjectiveTool)
admin.site.register(DefinitionOfGood)
admin.site.register(Task)
admin.site.register(Achievement)


