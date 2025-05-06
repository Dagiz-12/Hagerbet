from django.urls import path
from . import views
from django.views.generic import TemplateView


app_name = 'users'

# Note use of plural for list view and singular for detail view
urlpatterns = [
    path('', views.MainusersView.as_view(), name='main'),


    path('user/<int:pk>', views.UserDetailView.as_view(), name='user'),
    path('users/create/', views.UserCreate.as_view(), name='user_create'),
    path('user/<int:pk>/update/', views.UserUpdate.as_view(), name='user_update'),
    path('user/<int:pk>/delete/', views.UserDelete.as_view(), name='user_delete'),

]
