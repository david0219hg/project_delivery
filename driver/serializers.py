from rest_framework import serializers
from driver.models import Driver, DriverOrders


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = "__all__"


class DriverOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverOrders
        fields = "__all__"
