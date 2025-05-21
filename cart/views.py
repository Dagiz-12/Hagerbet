from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib import messages
from products.models import Products
from .utils import get_cart


class CartView(View):

    def get(self, request):
        cart = get_cart(request)
        # Convert cart items to include proper IDs
        cart_items = []
        for product_id, item_data in cart.cart.items():
            cart_items.append({
                'id': product_id,
                **item_data,
                'total': float(item_data['price']) * item_data['quantity']
            })
        return render(request, 'cart/carts_list.html', {'cart': cart_items})


class AddToCartView(View):
    def post(self, request, product_id):
        try:
            product = Products.objects.get(id=product_id)
            quantity = int(request.POST.get('quantity', 1))

            cart = get_cart(request)
            cart.add(product_id, {
                'name': product.product_name,
                'price': str(product.price),
                'image': product.image.url,
            }, quantity)

            messages.success(request, f"{product.product_name} added to cart")
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'count': len(cart),
                    'message': f"{product.product_name} added to cart"
                })
            return redirect('cart:view')

        except Products.DoesNotExist:
            messages.error(request, "Product not found")
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'Product not found'}, status=404)
            return redirect('home:home')


class UpdateCartView(View):
    def post(self, request, product_id):
        try:
            quantity = int(request.POST.get('quantity', 1))
            cart = get_cart(request)
            cart.update(product_id, quantity)
            return redirect('cart:view')
        except ValueError:
            return redirect('cart:view')


class RemoveFromCartView(View):
    def post(self, request, product_id):
        cart = get_cart(request)
        cart.remove(product_id)
        return redirect('cart:view')


class CartCountView(View):
    def get(self, request):
        cart = get_cart(request)
        return JsonResponse({'count': len(cart)})
