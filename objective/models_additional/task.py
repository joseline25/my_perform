from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# from objective.models import Objective
from . import general_model
import datetime as Date

# Create your models here.


class Achievement(general_model.Common_Info):
    achievement_name = models.CharField(max_length=400, blank=True, null=True)
    weight = models.IntegerField(null=True, blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, default=1, related_name='achievement_created_by')
    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, default=1, related_name='achievement_updated_by')

    def __str__(self) -> str:
        return self.achievement_name


class Task(models.Model):

    STATUS_CHOICE = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
        ("Review", "Review")
    ]
    # current_datetime = Date.datetime.now()
    taskCode = models.CharField(max_length=50, primary_key=True)
    summary = models.TextField(null=False, blank=True)
    achievement = models.ForeignKey(
        Achievement, on_delete=models.CASCADE, null=False, blank=False, db_column='achievement')
    duration = models.DecimalField(
        max_digits=10, decimal_places=3, null=False, blank=False)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICE, default="Pending")
    # supervisor=models.ForeignKey(Member, null=True, on_delete=models.SET_NULL,related_name='supervisor',blank=False,db_column='supervisor')
    # created_by = models.ForeignKey(Member,on_delete=models.SET_NULL,null=True,db_column='created_by')
    # objective=models.ForeignKey(Objective,on_delete=models.CASCADE,null=False,blank=False,db_column='objective')
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_by = models.ForeignKey(Member,on_delete=models.SET_NULL,null=True,db_column='updated_by',related_name='taskupdated_by')

    class Meta:
        db_table = 'Task'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.summary

    def taskCodeGenerator(self):
        # latesttask=(Task.objects.order_by('-taskcode')[0])
        # print(latesttask)
        # taskcode=latesttask.values('taskcode')[0]['taskcode']
        # print(taskcode)
        dateObject = Date.datetime.today()
        YEAR = dateObject.strftime("%y")
        MONTH = dateObject.strftime("%m")
        PREFIX = "CAAS"

        try:
            taskcode = Task.objects.latest('taskCode').pk
            index = taskcode[8:15]
            lastmonth = taskcode[6:8]
            if lastmonth != MONTH:
                index = 0
        except:
            index = 0
        num = int(index)
        num1 = str.format("{:0>7d}", num + 1)
        print(num, num1, index)
        code = PREFIX + YEAR + MONTH + num1
        return code


class Collaboration(models.Model):
    task = models.ForeignKey(
        Task, null=False, blank=False, db_column='task', on_delete=models.CASCADE)
    # member=models.ForeignKey(Member,null=False, on_delete=models.CASCADE,db_column='member',related_name="participants")

    class Meta:
        db_table = 'Collaboration'

    def __str__(self) -> str:
        return self.task
