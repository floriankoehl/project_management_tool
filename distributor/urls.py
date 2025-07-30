from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('teams', views.teams, name='teams'),
    path('tasks', views.tasks, name='tasks'),
    path('create_team', views.create_team, name='create_team'),
    path('create_task_page', views.create_task_page, name='create_task_page'),
    path('create_task', views.create_task, name='create_task'),
    path('define_project_timeframe', views.define_project_timeframe, name='define_project_timeframe'),
    path("change_project_page", views.change_project_page, name='change_project_page'),
    path('delete_task/<int:id>/', views.delete_task, name='delete_task'),
    path('add_dependency/<int:id>/', views.add_dependency, name='add_dependency'),
    path('add_dependency_page/<int:id>/', views.add_dependency_page, name='add_dependency_page'),
    path('delete_dependency/<int:id>/', views.delete_dependency, name='delete_dependency'),
    path('display_task/<int:id>/', views.display_task, name='display_task'),
    path('edit_task/<int:id>/', views.edit_task, name='edit_task'),

]