from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views import generic

from products.models import Catagories, Products
from products.forms import MakeForm


class MainView(LoginRequiredMixin, View):
    def get(self, request):
        pc = Catagories.objects.all().count()
        ca = Products.objects.all()

        ctx = {'catagories_count': pc, 'products_list': ca}
        return render(request, 'products/products_list.html', ctx)


class MakeView(LoginRequiredMixin, View):
    def get(self, request):
        ca = Catagories.objects.all()
        ctx = {'catagories_list': ca}
        return render(request, 'products/catagories_list.html', ctx)


class ProductsDetailView(LoginRequiredMixin, generic.DetailView):
    model = Products


# We use reverse_lazy() because we are in "constructor attribute" code
# that is run before urls.py is completely loaded
class MakeCreate(LoginRequiredMixin, View):
    template = 'products/catagories_form.html'
    success_url = reverse_lazy('products:all')

    def get(self, request):
        form = MakeForm()
        ctx = {'form': form}
        return render(request, self.template, ctx)

    def post(self, request):
        form = MakeForm(request.POST)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template, ctx)

        Make = form.save()
        return redirect(self.success_url)


# MakeUpdate has code to implement the get/post/validate/store flow
# AutoUpdate (below) is doing the same thing with no code
# and no form by extending UpdateView
class MakeUpdate(LoginRequiredMixin, View):
    model = Catagories
    success_url = reverse_lazy('autos:all')
    template = 'products/products_form.html'

    def get(self, request, pk):
        make = get_object_or_404(self.model, pk=pk)
        form = MakeForm(instance=make)
        ctx = {'form': form}
        return render(request, self.template, ctx)

    def post(self, request, pk):
        make = get_object_or_404(self.model, pk=pk)
        form = MakeForm(request.POST, instance=make)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template, ctx)

        form.save()
        return redirect(self.success_url)


class MakeDelete(LoginRequiredMixin, View):
    model = Catagories
    success_url = reverse_lazy('products:all')
    template = 'products/products_confirm_delete.html'

    def get(self, request, pk):
        make = get_object_or_404(self.model, pk=pk)
        form = MakeForm(instance=make)
        ctx = {'make': make}
        return render(request, self.template, ctx)

    def post(self, request, pk):
        make = get_object_or_404(self.model, pk=pk)
        make.delete()
        return redirect(self.success_url)


# Take the easy way out on the main table
# These views do not need a form because CreateView, etc.
# Build a form object dynamically based on the fields
# value in the constructor attributes
class AutoCreate(LoginRequiredMixin, CreateView):
    model = Products
    fields = '__all__'
    success_url = reverse_lazy('products:all')


class AutoUpdate(LoginRequiredMixin, UpdateView):
    model = Products
    fields = '__all__'
    success_url = reverse_lazy('products:all')


class AutoDelete(LoginRequiredMixin, DeleteView):
    model = Products
    fields = '__all__'
    success_url = reverse_lazy('products:all')

# We use reverse_lazy rather than reverse in the class attributes
# because views.py is loaded by urls.py and in urls.py as_view() causes
# the constructor for the view class to run before urls.py has been
# completely loaded and urlpatterns has been processed.

# References

# https://docs.djangoproject.com/en/3.0/ref/class-based-views/generic-editing/#createview
