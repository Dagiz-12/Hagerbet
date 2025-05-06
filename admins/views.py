from django.shortcuts import render
from django.views import View
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views import generic

# Create your views here.


class HomeView(View):
    def get(self, request):

        ca = Catagories.objects.all()
        pa = Products.objects.all()

        ctx = {'catagories': ca, 'products_list': pa}

        return render(request, 'home/admins.html', ctx)
