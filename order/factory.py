import factory
from order.models import Order


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order
