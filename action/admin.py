from django.contrib import admin

from .models import Actions, Question, Collaborator, ActionTool, ActionSkill, Achievement, ActionAchievement

# Register your models here.

admin.site.register(Actions)
admin.site.register(Question)
admin.site.register(Collaborator)
admin.site.register(ActionTool)
admin.site.register(ActionSkill)
admin.site.register(Achievement)
admin.site.register(ActionAchievement)