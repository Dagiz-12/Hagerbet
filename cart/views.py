from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from products.models import Products  # Import your Product model
import json


class CartView(LoginRequiredMixin, View):
    def get(self, request):
        cart = request.session.get('cart', {})
        cart_items = []
        subtotal = 0

        for product_id, item in cart.items():
            try:
                # Get the actual product from database
                product = Products.objects.get(id=product_id)
                cart_item = {
                    'id': product.id,
                    'name': product.product_name,
                    'price': float(product.price),
                    'image': product.image.url if product.image else '/static/images/default-product.jpg',
                    'quantity': item.get('quantity', 1),
                    'description': product.discription
                }
                cart_items.append(cart_item)
                subtotal += cart_item['price'] * cart_item['quantity']
            except Products.DoesNotExist:
                # Remove invalid product from cart
                del cart[product_id]
                request.session['cart'] = cart

        total = subtotal  # Add shipping/tax if needed

        context = {
            'cart_items': cart_items,
            'subtotal': "{:.2f}".format(subtotal),
            'total': "{:.2f}".format(total)
        }

        return render(request, 'cart/carts_list.html', context)

    def post(self, request):
        # Handle AJAX requests for cart updates
        try:
            data = json.loads(request.body)
            action = data.get('action')
            product_id = str(data.get('product_id'))

            cart = request.session.get('cart', {})

            if action == 'add':
                try:
                    product = Products.objects.get(id=product_id)
                    product_data = {
                        'id': product_id,
                        'name': product.product_name,
                        'price': float(product.price),
                        'image': product.image.url if product.image else '/static/images/default-product.jpg',
                        'quantity': int(data.get('quantity', 1)),
                        'description': product.discription
                    }

                    if product_id in cart:
                        cart[product_id]['quantity'] += product_data['quantity']
                    else:
                        cart[product_id] = product_data

                    request.session['cart'] = cart
                    return JsonResponse({
                        'status': 'success',
                        'cart_count': sum(item['quantity'] for item in cart.values())
                    })
                except Products.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Product not found'}, status=404)

            elif action == 'update':
                change = int(data.get('change', 0))
                if product_id in cart:
                    cart[product_id]['quantity'] += change
                    if cart[product_id]['quantity'] <= 0:
                        del cart[product_id]

                request.session['cart'] = cart
                return JsonResponse({
                    'status': 'success',
                    'cart_count': sum(item['quantity'] for item in cart.values())
                })

            elif action == 'remove':
                if product_id in cart:
                    del cart[product_id]
                    request.session['cart'] = cart

                return JsonResponse({
                    'status': 'success',
                    'cart_count': sum(item['quantity'] for item in cart.values())
                })

            return JsonResponse({'status': 'error', 'message': 'Invalid action'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)


class CartCountView(View):
    def get(self, request):
        cart = request.session.get('cart', {})
        return JsonResponse({
            'count': sum(item['quantity'] for item in cart.values())
        })


class CartSummaryView(View):
    def get(self, request):
        cart = request.session.get('cart', {})
        subtotal = sum(
            float(item['price']) * item['quantity']
            for item in cart.values()
        )
        total = subtotal  # Add shipping/tax if needed

        return JsonResponse({
            'status': 'success',
            'subtotal': subtotal,
            'total': total
        })
