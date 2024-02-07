from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from . import general_model
import datetime as Date

# Create your models here.


class Task(models.Model):

    STATUS_CHOICE = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
        ("Review", "Review")
    ]

    achievements_type = [("Work-Product", "Work-Product"), ("Deliverable",
                                                            "Deliverable"), ("Learning", "Learning"), ("Miscellaneous", "Miscellaneous")]
    taskCode = models.CharField(max_length=50)
    summary = models.TextField(null=False, blank=True)
    achievement = models.CharField(
        max_length=100, choices=achievements_type, default="Deliverable")
    duration = models.DecimalField(
        max_digits=10, decimal_places=3, null=False, blank=False)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICE, default="Pending")

    created_at = models.DateTimeField(auto_now_add=True)
    # updated_by = models.ForeignKey(Member,on_delete=models.SET_NULL,null=True,db_column='updated_by',related_name='taskupdated_by')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.taskCode


class Collaboration(models.Model):
    task = models.ForeignKey(
        Task, null=False, blank=False, db_column='task', on_delete=models.CASCADE)
    members = models.ManyToManyField(
        User, related_name="collaborations")

    def __str__(self):
        return self.task
