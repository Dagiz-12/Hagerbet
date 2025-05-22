from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, View, ListView
from django.urls import reverse_lazy
from django.contrib import messages

from .models import CustomUser
from .forms import CustomerRegistrationForm, AdminUserCreationForm
from .models import ActivityLog
import json
from django.http import JsonResponse
from django.shortcuts import redirect


#  mixins


class StaffRequiredMixin(LoginRequiredMixin):
    """Verify that the current user is staff or admin."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if request.user.role not in [CustomUser.Role.ADMIN, CustomUser.Role.STAFF]:
            messages.error(
                request, "You don't have permission to access this page.")
            # Redirect to home or appropriate page
            return redirect('profiles:customer_profile')

        return super().dispatch(request, *args, **kwargs)


class CustomerAccessMixin:
    """Ensure users can only access their own data."""

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.role == CustomUser.Role.CUSTOMER:
            return qs.filter(id=self.request.user.id)
        return qs


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


class AdminUserCreateView(StaffRequiredMixin, CreateView):
    model = CustomUser
    form_class = AdminUserCreationForm
    template_name = 'users/admin_user_form.html'
    success_url = reverse_lazy('users:main')

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.role == CustomUser.Role.ADMIN

    def form_valid(self, form):
        response = super().form_valid(form)
        ActivityLog.objects.create(
            user=self.request.user,
            action=f"Created user {self.object.email}",
            details=json.dumps({
                'email': self.object.email,
                'role': self.object.role
            })
        )
        return response


class UserDetailView(DetailView):
    model = CustomUser
    template_name = 'users/users_detail.html'  # Make sure this template exists
    context_object_name = 'user'


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CustomUser
    fields = ['first_name', 'last_name', 'email', 'phone', 'address']
    template_name = 'users/users_form.html'
    success_url = reverse_lazy('users:main')

    def test_func(self):
        return self.request.user == self.get_object() or self.request.user.role in [CustomUser.Role.ADMIN, CustomUser.Role.STAFF]


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CustomUser
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('users:main')

    def test_func(self):
        # Only allow admins to delete users
        return self.request.user.is_superuser


class MainusersView(StaffRequiredMixin, ListView):
    model = CustomUser
    template_name = 'users/main.html'
    context_object_name = 'users_list'

    def get_queryset(self):
        if self.request.user.role == CustomUser.Role.ADMIN:
            return CustomUser.objects.all()
        return CustomUser.objects.filter(role=CustomUser.Role.CUSTOMER)


class ActivityLogView(StaffRequiredMixin, ListView):
    model = ActivityLog
    template_name = 'users/activity_log.html'
    context_object_name = 'logs'
    paginate_by = 20

    def get_queryset(self):
        return ActivityLog.objects.all().order_by('-timestamp')


class StaffRegisterView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = CustomUser
    form_class = AdminUserCreationForm
    template_name = 'users/staff_register.html'
    success_url = reverse_lazy('users:main')

    def test_func(self):
        # Only allow admins to create staff
        return self.request.user.role == CustomUser.Role.ADMIN

    def form_valid(self, form):
        user = form.save(commit=False)
        user.role = CustomUser.Role.STAFF
        user.is_staff = True
        user.save()
        messages.success(
            self.request, f'Staff user {user.email} created successfully!')
        return super().form_valid(form)
