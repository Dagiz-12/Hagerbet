from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import CustomerProfileView, ProfileUpdateView

app_name = 'profiles'

urlpatterns = [
    path('', CustomerProfileView.as_view(), name='customer_profile'),
    path('update/', ProfileUpdateView.as_view(), name='profile_update'),
]
