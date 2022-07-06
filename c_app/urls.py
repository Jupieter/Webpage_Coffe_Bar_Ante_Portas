from django.urls import path
from . import views

app_name = 'c_app'

urlpatterns = [
    path('', views.all_tasks, name='all_tasks'),
    path('create', views.create_task, name='create_task')
]