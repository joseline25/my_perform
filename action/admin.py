from django.contrib import admin
from action.models import Action, ActionTool, ActionSkill
from action.models import Question

admin.site.register(Action)
admin.site.register(ActionTool)
admin.site.register(ActionSkill)
admin.site.register(Question)
