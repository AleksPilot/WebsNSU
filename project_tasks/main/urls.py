from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('new_task', views.new_task, name='new_task'),
]
