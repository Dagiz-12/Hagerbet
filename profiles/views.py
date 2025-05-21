from django.shortcuts import render
from django.views import View
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.views import generic
from users.models import CustomUser
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class CustomerProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profiles/profiles.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['customer'] = user  # Make sure to pass the user as 'customer'

        # Get orders if the relationship exists
        if hasattr(user, 'orders'):
            context['orders'] = user.orders.all()
        else:
            context['orders'] = []

        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ['first_name', 'last_name', 'email', 'phone']
    template_name = 'profiles/profile_update.html'
    # Updated to match your URL name
    success_url = reverse_lazy('profiles:customer_profile')

    def get_object(self):
        return self.request.user
    # This will ensure that the user can only update their own profile
