from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
  path('sign_in', views.my_login, name = 'sign_in'),
  # path('sign_up', views.signup_render, name = 'sign_up'),
  path('',views.home_render, name = 'homepage'),
  path('register',views.register, name= 'perform_register'),
  path('perform_login', views.perform_login, name = 'perform_login'),
  path('perform_logout', views.perform_logout, name= 'perform_logout'),
  path('adminDash', views.adminDashboard, name= 'adminDash'),
  path('perform_admin', views.admin_login, name= 'perform_admin'),
  path('delete/<int:pk>/', views.delete, name='delete_user'),
  path('edit_user/<int:pk>/', views.edit_user, name='edit_user')
]
