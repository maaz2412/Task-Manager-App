from django.urls import path
from .import views
urlpatterns = [
    path('landing-page/',views.landing_page, name='landing-page'),
    path('home/', views.home_page, name='home'),
    path('tasks/', views.tasks, name='tasks'),
    path('finished/<str:name>/', views.finished, name='finished'),
    path('register/', views.register, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('delete/<str:name>/', views.delete_task, name='delete')
]