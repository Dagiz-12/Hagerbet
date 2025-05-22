from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views import generic

from products.models import Catagories, Products
from products.forms import MakeForm

from users.views import StaffRequiredMixin
from django.contrib import messages
import json
from users.models import ActivityLog


class MainView(StaffRequiredMixin, View):
    def get(self, request):
        pc = Catagories.objects.all().count()
        ca = Products.objects.all()

        ActivityLog.objects.create(
            user=request.user,
            action="Viewed products dashboard",
            details=json.dumps({
                'categories_count': pc,
                'products_count': ca.count()
            })
        )

        ctx = {'catagories_count': pc, 'products_list': ca}
        return render(request, 'products/products_list.html', ctx)


class MakeView(StaffRequiredMixin, View):
    def get(self, request):
        ca = Catagories.objects.all()
        ctx = {'catagories_list': ca}
        return render(request, 'products/catagories_list.html', ctx)


class ProductsDetailView(StaffRequiredMixin, generic.DetailView):
    model = Products


# We use reverse_lazy() because we are in "constructor attribute" code
# that is run before urls.py is completely loaded
class MakeCreate(StaffRequiredMixin, View):
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

        ActivityLog.objects.create(
            user=request.user,
            action=f"Created category: {Make.name}",
            details=json.dumps({
                'category_id': Make.id,
                'category_name': Make.name
            })
        )

        messages.success(
            request, f"Category '{Make.name}' created successfully!")
        return redirect(self.success_url)


# MakeUpdate has code to implement the get/post/validate/store flow
# AutoUpdate (below) is doing the same thing with no code
# and no form by extending UpdateView
class MakeUpdate(StaffRequiredMixin, View):
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

    def form_valid(self, form):
        response = super().form_valid(form)

        ActivityLog.objects.create(
            user=self.request.user,
            action=f"Created product: {self.object.product_name}",
            details=json.dumps({
                'product_id': self.object.id,
                'product_name': self.object.product_name,
                'price': str(self.object.price)
            })
        )

        messages.success(
            self.request, f"Product '{self.object.product_name}' created successfully!")
        return response


class MakeDelete(StaffRequiredMixin, View):
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

    def form_valid(self, form):
        response = super().form_valid(form)

        ActivityLog.objects.create(
            user=self.request.user,
            action=f"Created product: {self.object.product_name}",
            details=json.dumps({
                'product_id': self.object.id,
                'product_name': self.object.product_name,
                'price': str(self.object.price)
            })
        )

        messages.success(
            self.request, f"Product '{self.object.product_name}' created successfully!")
        return response


# Take the easy way out on the main table
# These views do not need a form because CreateView, etc.
# Build a form object dynamically based on the fields
# value in the constructor attributes
class AutoCreate(StaffRequiredMixin, CreateView):
    model = Products
    fields = '__all__'
    success_url = reverse_lazy('products:all')

    def form_valid(self, form):
        response = super().form_valid(form)

        ActivityLog.objects.create(
            user=self.request.user,
            action=f"Created product: {self.object.product_name}",
            details=json.dumps({
                'product_id': self.object.id,
                'product_name': self.object.product_name,
                'price': str(self.object.price)
            })
        )

        messages.success(
            self.request, f"Product '{self.object.product_name}' created successfully!")
        return response


class AutoUpdate(StaffRequiredMixin, UpdateView):
    model = Products
    fields = '__all__'
    success_url = reverse_lazy('products:all')

    def form_valid(self, form):
        response = super().form_valid(form)

        ActivityLog.objects.create(
            user=self.request.user,
            action=f"Created product: {self.object.product_name}",
            details=json.dumps({
                'product_id': self.object.id,
                'product_name': self.object.product_name,
                'price': str(self.object.price)
            })
        )

        messages.success(
            self.request, f"Product '{self.object.product_name}' created successfully!")
        return response


class AutoDelete(StaffRequiredMixin, DeleteView):
    model = Products
    fields = '__all__'
    success_url = reverse_lazy('products:all')

    def form_valid(self, form):
        response = super().form_valid(form)

        ActivityLog.objects.create(
            user=self.request.user,
            action=f"Created product: {self.object.product_name}",
            details=json.dumps({
                'product_id': self.object.id,
                'product_name': self.object.product_name,
                'price': str(self.object.price)
            })
        )

        messages.success(
            self.request, f"Product '{self.object.product_name}' created successfully!")
        return response

# We use reverse_lazy rather than reverse in the class attributes
# because views.py is loaded by urls.py and in urls.py as_view() causes
# the constructor for the view class to run before urls.py has been
# completely loaded and urlpatterns has been processed.

# References

# https://docs.djangoproject.com/en/3.0/ref/class-based-views/generic-editing/#createview
