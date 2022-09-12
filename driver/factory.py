import factory
from driver.models import Driver, DriverOrders


class DriverFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Driver


class DriverOrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DriverOrders
