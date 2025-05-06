from django.shortcuts import render, get_object_or_404
from django.views import View
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.detail import DetailView

from products.models import Catagories, Products
from users.models import Users

# views.py
from django.http import JsonResponse


def product_api(request, slug):
    try:
        product = Products.objects.get(slug=slug)
        data = {
            'id': product.id,
            'slug': product.slug,
            'name': product.product_name,
            'price': float(product.price),
            'image': product.image.url,
            'description': product.description
        }
        return JsonResponse(data)
    except Products.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)


class HomeView(View):
    def get(self, request):
        ca = Catagories.objects.all()
        pa = Products.objects.all()
        ctx = {'catagories': ca, 'products_list': pa}
        return render(request, 'home/index.html', ctx)


class ProductsDetailView(View):
    def get(self, request, slug):
        product = get_object_or_404(Products, slug=slug)
        context = {'product': product}
        return render(request, 'home/products_detail.html', context)
