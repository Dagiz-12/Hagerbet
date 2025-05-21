from django.urls import path
from .views import CustomerProfileView, ProfileUpdateView

app_name = 'profiles'

urlpatterns = [
    # This is your profile view
    path('', CustomerProfileView.as_view(), name='customer_profile'),
    path('update/', ProfileUpdateView.as_view(), name='profile_update'),
]
