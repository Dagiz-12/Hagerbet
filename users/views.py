from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, View, ListView
from django.urls import reverse_lazy
from django.contrib import messages

from .models import CustomUser
from .forms import CustomerRegistrationForm, AdminUserCreationForm


class CustomerRegisterView(CreateView):
    model = CustomUser
    form_class = CustomerRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('home')  # Change to your home URL

    def form_valid(self, form):
        # Force customer role
        user = form.save(commit=False)
        user.role = CustomUser.Role.CUSTOMER
        user.username = user.email  # Set username same as email
        user.save()

        # Auto-login after registration (optional)
        login(self.request, user)
        messages.success(self.request, 'Registration successful!')
        return super().form_valid(form)


class AdminUserCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = CustomUser
    form_class = AdminUserCreationForm
    template_name = 'users/admin_user_form.html'
    success_url = reverse_lazy('users:main')

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.role == CustomUser.Role.ADMIN

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, f'User {self.object.email} created successfully!')
        return response


class UserDetailView(DetailView):
    model = CustomUser
    template_name = 'users/users_detail.html'  # Make sure this template exists
    context_object_name = 'user'


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CustomUser
    fields = ['first_name', 'last_name', 'email', 'phone', 'address']
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:main')

    def test_func(self):
        # Only allow users to edit their own profile or admins
        return self.request.user == self.get_object() or self.request.user.is_superuser


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CustomUser
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('users:main')

    def test_func(self):
        # Only allow admins to delete users
        return self.request.user.is_superuser


class MainusersView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = 'users/main.html'
    context_object_name = 'users_list'

    def get_queryset(self):
        # For non-admins, only show their own profile
        if not self.request.user.is_superuser:
            return CustomUser.objects.filter(id=self.request.user.id)
        return CustomUser.objects.all()
