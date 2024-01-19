from django.db import models
from objective.models import Objective


class Question(models.Model):
    question = models.TextField(null=True, blank=True)
    objective = models.ForeignKey(Objective, on_delete=models.PROTECT, null=True)
    number = models.IntegerField(null=True,)
    answer = models.BooleanField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.question