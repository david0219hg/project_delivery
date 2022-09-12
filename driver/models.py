from django.db import models
from order.models import Order


class Driver(models.Model):
    orders = models.ManyToManyField(Order, through="DriverOrders")
    free = models.BooleanField(default=True)
    length_driver = models.FloatField(default=0)
    latitude_driver = models.FloatField(default=0)
    updated_at = models.DateTimeField(null=True)


class DriverOrders(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField()
    active = models.BooleanField(default=False)
