from decimal import Decimal

from shoppingcart.models import Product

KEY = 'SHOPPING-CART'

class Cart:
    def __init__(self, request):
        self.cart = request.session.get(KEY, {})
        self.request = request

    def add(self, product_id, quantity=1):
        if product_id in self.cart:
            self.cart[product_id] += quantity
        else:
            self.cart[product_id] = quantity
        self._update_session()

    def update(self, product_id, quantity):
        if product_id in self.cart:
            if int(quantity) == 0:
                self.cart.pop(product_id)
            else:
                self.cart[product_id] = quantity
        self._update_session()

    def clear(self):
        self.cart = {}
        self._update_session()

    def total(self):
        total = Decimal(0)
        print self.cart
        for product_id in self.cart:
            price = Product.objects.get(id=product_id).price
            total += price * Decimal(self.cart[product_id])
        return total

    def _update_session(self):
        self.request.session[KEY] = self.cart