from .utils import get_cart


def cart(request):
    return {
        'cart_count': len(get_cart(request))
    }
