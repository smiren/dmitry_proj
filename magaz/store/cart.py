from store.models import Product
from magaz import settings

from decimal import Decimal


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.setdefault(settings.SESSION_CART_NAME, {})
        self.price = self.get_total_price()

    def add(self, product, quantity=1, update=False):
        prod = self.cart.setdefault(str(product.pk), {
            'price': str(product.price),
            'name': product.name,
            'slug': product.slug,
            'id': product.pk,
            'url': product.get_absolute_url(),
        })
        prod['quantity'] = quantity if update \
            else prod.get('quantity', 0) + quantity
        self.save()

    def remove(self, product):
        if str(product.pk) in self.cart:
            del self.cart[str(product.pk)]
            self.save()

    def __iter__(self):
        for item in self.cart.values():
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_queryset(self):
        return Product.objects.filter(pk__in=self.cart.keys())

    def objects_iter(self):
        for product in self.get_queryset():
            quantity = self.cart.get(str(product.pk)).get('quantity')
            yield {
                'product': product,
                'quantity': quantity,
                'cost': product.price*quantity
            }

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def save(self):
        self.price = self.get_total_price()
        self.session.save()

    def clear(self):
        self.cart.clear()
        self.save()
