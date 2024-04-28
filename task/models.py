from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=None, null=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=600)
    status = models.BooleanField(default=False)
    category = models.CharField(max_length=40, default=None, null=True)

    def __str__(self):
        return self.name