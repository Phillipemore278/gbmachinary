from decimal import Decimal

from django.conf import settings
from store.models import Product


class Basket:
    
    def __init__(self, request):
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if settings.BASKET_SESSION_ID not in request.session:
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        self.basket = basket

    def add(self, product, qty):
        product_id = str(product.id)

        if product_id in self.basket:
            pass
        else:
            self.basket[product_id] = {"price": str(product.price), 'qty':qty}
        self.save()

    def __iter__(self):
        product_ids = self.basket.keys()
        products = Product.objects.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]["product"] = product

        for item in basket.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["qty"]
            yield item

    def __len__(self):
        return sum(item["qty"] for item in self.basket.values())
    
    def get_subtotal_price(self):
        return sum(Decimal(item["price"]) * item["qty"] for item in self.basket.values())
    
    def get_total_price(self):

        subtotal = sum(Decimal(item["price"]) * item["qty"] for item in self.basket.values())

        # if subtotal <= 25000 :
        #     shipping = Decimal(0.00)
        # elif subtotal <= 55000:
        #     shipping = Decimal(10000.00)
        # elif subtotal <= 120000:
        #     shipping = Decimal(20500.00)
        # elif subtotal <= 270000:
        #     shipping = Decimal(27500.00)
        # elif subtotal <= 330000:
        #     shipping = Decimal(32000.00)
        # elif subtotal <= 470000:
        #     shipping = Decimal(34000.00)
        # else:
        #     shipping = Decimal(49500.50)

        # total = subtotal + Decimal(shipping)
        total = subtotal
        return total
    

    def get_shipping_price(self):
        subtotal = sum(Decimal(item["price"]) * item["qty"] for item in self.basket.values())
        if subtotal <= 25000 :
            shipping = Decimal(0.00)
        elif subtotal <= 55000:
            shipping = Decimal(10000.00)
        elif subtotal <= 120000:
            shipping = Decimal(20500.00)
        elif subtotal <= 270000:
            shipping = Decimal(27500.00)
        elif subtotal <= 330000:
            shipping = Decimal(32000.00)
        elif subtotal <= 470000:
            shipping = Decimal(34000.00)
        else:
            shipping = Decimal(49500.50)
        return shipping
    
    
    def delete(self, product):
        product_id = str(product)

        if product_id in self.basket:
            del self.basket[product_id]
            self.save()

    def clear(self):
        # Remove basket from session
        del self.session[settings.BASKET_SESSION_ID]
        self.save()

    def save(self):
        self.session.modified = True