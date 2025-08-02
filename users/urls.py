from django.urls import path
from . import views

urlpatterns = [
    path('teams', views.teams, name='teams'),
    path('create_team', views.create_team, name='create_team'),
    path('delete_team/<int:id>/', views.delete_team, name='delete_team'),
    path('edit_team_page/<int:id>/', views.edit_team_page, name='edit_team_page'),
    path('team_update_name/<int:id>/', views.team_update_name, name='team_update_name'),
    path('team_update_color/<int:id>/', views.team_update_color, name='team_update_color'),
    path('register_view', views.register_view, name='register_view'),
    path('register_user', views.register_user, name='register_user'),
    path('login_view', views.login_view, name='login_view'),
    path('logout_view', views.logout_view, name='logout_view'),
]