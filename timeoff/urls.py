from django.urls import path
from . import views

urlpatterns = [
    path('team/', views.team_status, name='team-status'),
    path('my-leaves/', views.my_leaves, name='my-leaves'),
    path('request/', views.request_leave, name='request-leave'),
]