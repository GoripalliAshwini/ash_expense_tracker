#from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
path('', views.index, name='index'),
path('dashboard/', views.dashboard, name='dashboard'),
path('add_transaction/', views.add_transaction, name='add_transaction'),    
path('reports/', views.reports, name='reports'),
path('history/', views.history, name='history'),    
path('edit/<int:id>/', views.edit_transaction, name='edit_transaction'),
path('delete/<int:id>/', views.delete_transaction, name='delete_transaction'),
path('login/', views.login_view, name='login_view'),
path('register/', views.register_view, name='register_view'),
path('logout/', views.logout_view, name='logout_view'),
]