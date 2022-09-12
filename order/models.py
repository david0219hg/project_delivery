from django.db import models


class Order(models.Model):
    date_time_arrive = models.DateTimeField(null=True)
    date_time_delivery = models.DateTimeField(null=True)
    latitude_arrrive = models.FloatField(default=0)
    length_arrrive = models.FloatField(default=0)
    latitude_delivery = models.FloatField(default=0)
    length_delivery = models.FloatField(default=0)
