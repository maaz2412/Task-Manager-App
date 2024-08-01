from django.shortcuts import render, redirect , get_object_or_404
from .models import Task
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

#Cookie setting view for filtering results
def set_cookie(request):
    if request.method == 'POST':
        filter_value = request.POST.get('filter', 'all')
        response = redirect('task_list')
        response.set_cookie('task_filter', filter_value, max_age=30*24*60*60,
                             httponly=True,       # Make the cookie HTTPOnly
            secure=True,)
        return response
#Filtered Results(displayed based on value from cookie)
def task_list(request):
    filter_value = request.COOKIES.get('task_filter')
    if filter_value == 'completed':
        tasks = Task.objects.filter(status=True)
    elif filter_value == 'incomplete':
        tasks = Task.objects.filter(status=False)
    else:
        tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks, 'filter_value': filter_value})
#Landing Page view(renders a template)
def landing_page(request):
    return render(request, 'landing_page.html')
#Main home page(user can add tasks, includes login required)
@login_required(login_url='login')
def home_page(request):
    if request.method == 'POST':
        # If form is submitted, handle the task creation
        task_name = request.POST.get('task-name')
        task_description = request.POST.get('task-description')
        category_value = request.POST.get('category')  # Assuming 'category' is the name of your select input
        user = request.user
        # Create a new Task object with the selected category
        new_task = Task(name=task_name, description=task_description, category=category_value, user=user)
        new_task.save()
        response = redirect('home')
        response.set_cookie('task-name', task_name)
        return response
    else:
        # Fetch categories from the database
        categories = Task.Category.choices  # Assuming Task is your model
        task_name = request.COOKIES.get('task-name', None )

        return render(request, 'home.html', {'categories': categories, 'task_name' : task_name})

#To mark tasks as completed
def finished(request, name):
    user = request.user
    tasks_finished = Task.objects.get(user=user, name=name)
    tasks_finished.status = True
    print("true")
    tasks_finished.save()
    return redirect('tasks')
#user registration
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirmation = request.POST.get('confirm_password')
        new_user = User.objects.create_user(username=username, password=password)
        new_user.save()
        if password == password_confirmation:
            valid_user = authenticate(request, username=username, password=password)
            if valid_user:
                login(request,valid_user)
                messages.success(request, 'Welcome Aboard')
                return redirect('home')
        else:
            messages.error(request, 'Please create an account','Recheck both passwords')
            return redirect('register')
    return render(request, 'register.html')

#Login view 
def login_page(request):
    if request.method == 'POST':
        username= request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('confirm_password')
        if password == password2:
            login_user = authenticate(request, username=username, password=password)
            if login_user is not None:
                login(request,login_user)
                print("User is logged in")
                messages.success(request, 'Welcome aboard')
                return redirect('home')
        else:
            messages.error(request, 'Wrong credential')
            return redirect('login')
    return render(request, 'login.html')
#logout view
def logout_user(request):
    logout(request)
    response = redirect('login')
    response.delete_cookie('task-name')
    return response
#Delete any task
def delete_task(request, pk):
    user = request.user
    to_be_deleted = Task.objects.get(user=user, pk=pk)
    to_be_deleted.delete()
    return redirect('task_list')
#Edit a task
def edit_task(request, pk):
    user = request.user
    task_to_edit = Task.objects.get(user=user , pk=pk)
    categories = Task.Category.choices
    if request.method == 'POST':
         task_to_edit.name = request.POST.get('task-name')
         task_to_edit.description = request.POST.get('task-description')
         task_to_edit.category = request.POST.get('category') 
        # Assuming 'category' is the name of your select input
         task_id = task_to_edit.id
         request.session['task_name'] = {task_id : task_to_edit.name}
         task_to_edit.save()
         return redirect('task_list')
    
    return render(request,'edit.html', {'categories': categories})




