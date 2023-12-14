from django.db import models
from models import Actions

class Question(models.Model):
    question = models.TextField(null=True, blank=True)
    number = models.IntegerField(null=True,)
    answer = models.BooleanField(null=True)
    related_action = models.ForeignKey(Actions, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.question