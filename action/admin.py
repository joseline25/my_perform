from django.contrib import admin
from action.models import Action, ActionTool, ActionSkill, Question, ActionMainEntry


admin.site.register(Action)
admin.site.register(ActionMainEntry)
admin.site.register(ActionTool)
admin.site.register(ActionSkill)
admin.site.register(Question)
