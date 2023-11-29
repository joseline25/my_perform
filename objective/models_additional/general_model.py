from django.db import models
import uuid


class Common_Info(models.Model):
    """This class is a Common model class that contains some basic fields that are common to most models"""
    id=models.UUIDField(primary_key=True,editable=False, default=uuid.uuid4) #UUIDField is a special field to store universally unique identifiers, it is a python library that helps in generating random objects of 128 bits as ids
    name=models.CharField(max_length=250,null=False,blank=False)
    description=models.TextField(null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
    def __str__(self) -> str:
        return self.name