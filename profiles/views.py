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
from orders.models import Orders
from .models import CustomerProfile
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import ProfileUpdateForm


class CustomerProfileView(LoginRequiredMixin, DetailView):
    model = CustomerProfile
    template_name = 'profiles/profiles.html'
    context_object_name = 'profile'

    def get_object(self):
        # Ensure users can only view their own profile
        profile, created = CustomerProfile.objects.get_or_create(
            user=self.request.user
        )
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Add additional context
        context['customer'] = user
        context['orders'] = Orders.objects.filter(
            user=user).order_by('-order_date')[:5]  # Last 5 orders

        # Check if user is customer (optional)
        if user.role != CustomUser.Role.CUSTOMER:
            messages.warning(
                self.request,
                "You're viewing this page as a non-customer user"
            )

        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ProfileUpdateForm
    template_name = 'profiles/profile_update.html'
    success_url = reverse_lazy('profiles:customer_profile')

    def get_object(self):
        return self.request.user.customer_profile
    # Ensure users can only update their own profile

    def form_valid(self, form):
        messages.success(self.request, "Profile updated successfully!")
        return super().form_valid(form)
