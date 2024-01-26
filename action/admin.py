from django.contrib import admin

from .models import Action, Question, ActionTool, ActionSkill, Achievement, ActionAchievement

# Register your models here.

admin.site.register(Action)
admin.site.register(Question)
admin.site.register(ActionTool)
admin.site.register(ActionSkill)
admin.site.register(Achievement)
admin.site.register(ActionAchievement)