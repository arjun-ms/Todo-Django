from django.urls import path
from . import views

urlpatterns = [
    path('',views.login, name='login'),
    path('register',views.register, name='register'),
    path('logout',views.logout, name='logout'),
    path('create',views.create, name='create'),
    path('home',views.home, name='home'),
    path('completed',views.completed, name='completed'),
    # path('modify',views.modify, name='modify')
    
]