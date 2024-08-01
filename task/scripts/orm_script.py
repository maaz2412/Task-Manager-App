from task.models import  Task
from django.contrib.auth.models import User

def run():
    Task.objects.all().delete()