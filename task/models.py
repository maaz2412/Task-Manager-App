from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    name = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=600)
    status = models.BooleanField(default=False)

    class Category(models.TextChoices):
        WORK = 'WK', 'Work'
        STUDY = 'ST', 'Study'
        PERSONAL = 'PR', 'Personal'

    category = models.CharField(
        max_length=2,
        choices=Category.choices,
        default=Category.PERSONAL,
    )

    def __str__(self):
        return self.name
