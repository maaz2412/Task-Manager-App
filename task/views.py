from django.shortcuts import render, redirect
from .models import Task
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
def landing_page(request):
    return render(request, 'landing_page.html')
@login_required(login_url='login')
def home_page(request):
    if request.method == 'POST':
        task_name = request.POST.get('task-name')
        task_description = request.POST.get('task-description')
        category = request.POST.get('category')
        user = request.user
        new_task = Task(name = task_name, description=task_description, category=category, user=user)
        new_task.save()
        print("Task saved")
    return render(request, 'home.html')


@login_required(login_url='login')
def tasks(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks.html' , {'tasks': tasks})
def finished(request, name):
    user = request.user
    tasks_finished = Task.objects.get(user=user, name=name)
    tasks_finished.status = True
    print("true")
    tasks_finished.save()
    return redirect('tasks')
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('confirm_password')
        new_user = User.objects.create_user(username=username, password=password)
        new_user.save()
        valid_user = authenticate(request, username=username, password=password)
        if valid_user:
            login(request,valid_user)
            messages.success(request, 'Welcome Aboard')
            return redirect('home')
        else:
            message = messages.error(request, 'Please create an account')
            return redirect('register')
    return render(request, 'register.html')
def login_page(request):
    if request.method == 'POST':
        username= request.POST.get('username')
        password = request.POST.get('password')
        print("Got Data")
        login_user = authenticate(request, username=username, password=password)
        print("User is authenticated")
        if login_user is not None:
            login(request,login_user)
            print("User is logged in")
            messages.success(request, 'Welcome aboard')
            return redirect('home')
        else:
            messages.error(request, 'Wrong credential')
            return redirect('login')
    return render(request, 'login.html')
def logout_user(request):
    logout(request)
    return redirect('login')
def delete_task(request, name):
    user = request.user
    tobe_deleted = Task.objects.get(user=user, name=name)
    tobe_deleted.delete()
    return redirect('tasks')
