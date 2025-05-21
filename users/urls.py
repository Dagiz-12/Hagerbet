from django.urls import path
from .views import (
    CustomerRegisterView,
    AdminUserCreateView,
    UserDetailView,
    UserUpdateView,
    UserDeleteView,
    MainusersView
)

app_name = 'users'
urlpatterns = [
    path('', MainusersView.as_view(), name='main'),
    path('register/', CustomerRegisterView.as_view(), name='register'),
    path('create/', AdminUserCreateView.as_view(), name='create'),
    path('<int:pk>/', UserDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='delete'),
]
