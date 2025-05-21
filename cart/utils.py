from django.conf import settings
import json


class CartItem:
    def __init__(self, product_id, name, price, image, quantity=1):
        self.id = product_id
        self.name = name
        self.price = float(price)
        self.image = image
        self.quantity = quantity

    @property
    def total_price(self):
        return self.price * self.quantity

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'image': self.image,
            'quantity': self.quantity
        }


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart or not isinstance(cart, dict):  # Add type check
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product_id, product_data, quantity=1):
        product_id = str(product_id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] += quantity
        else:
            self.cart[product_id] = {
                'quantity': quantity,
                **product_data
            }
        self.save()

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def update(self, product_id, quantity):
        product_id = str(product_id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = max(0, quantity)
            if self.cart[product_id]['quantity'] <= 0:
                del self.cart[product_id]
            self.save()

    def clear(self):
        """Remove all items from the cart"""
        try:
            del self.session[settings.CART_SESSION_ID]
            self.save()
        except KeyError:
            pass  # Cart was already empty

    def save(self):
        self.session.modified = True

    def __iter__(self):
        return iter(self.cart.values())

    def __len__(self):
        if not isinstance(self.cart, dict):  # Handle case where cart isn't a dict
            return 0
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        if not isinstance(self.cart, dict):  # Handle case where cart isn't a dict
            return 0
        return sum(float(item['price']) * item['quantity'] for item in self.cart.values())


def get_cart(request):
    return Cart(request)


def clear_cart(request):
    cart = Cart(request)
    cart.clear()  # Now this will work since we've added the clear() method
