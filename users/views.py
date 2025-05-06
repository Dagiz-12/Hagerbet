from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views import generic

from users.models import Users


class MainusersView(LoginRequiredMixin, View):
    def get(self, request):
        us = Users.objects.all()

        ctx = {'users_list': us}
        return render(request, 'users/main.html', ctx)


class UserDetailView(LoginRequiredMixin, generic.DetailView):
    model = Users


class UserCreate(CreateView):
    model = Users
    fields = '__all__'
    success_url = reverse_lazy('users:main')


class UserUpdate(LoginRequiredMixin, UpdateView):
    model = Users
    fields = '__all__'
    success_url = reverse_lazy('users:main')


class UserDelete(LoginRequiredMixin, DeleteView):
    model = Users
    fields = '__all__'
    success_url = reverse_lazy('users:main')
