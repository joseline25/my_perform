from django.contrib import admin
from action.models import Action, ActionAchievement, ActionTool, ActionSkill, Achievement
from action.models import Question

admin.site.register(Action)
admin.site.register(ActionAchievement)
admin.site.register(ActionTool)
admin.site.register(ActionSkill)
admin.site.register(Achievement)
admin.site.register(Question)

