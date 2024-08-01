from django.urls import path
from .import views
urlpatterns = [
    path('landing-page/',views.landing_page, name='landing-page'),
    path('home/', views.home_page, name='home'),
    path('finished/<str:name>/', views.finished, name='finished'),
    path('register/', views.register, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('delete/<int:pk>/', views.delete_task, name='delete'),
    path('edit/<int:pk>/', views.edit_task, name='edit'),
    path('set_task_filter/', views.set_cookie, name='set_cookie'),
    path('task_list/', views.task_list, name='task_list'),
]