from django.urls import path
from . import views

urlpatterns = [
    path('', views.item_list, name='item-list'),
    path('my-inventory/', views.my_items, name='my-items'),
    path('new/', views.item_create, name='item-create'),
    path('<int:pk>/request/', views.request_item, name='request-item'),
    path('requests/', views.my_requests, name='my-requests'),
    path('requests/<int:pk>/<str:action>/', views.respond_request, name='respond-request'),
]