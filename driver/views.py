import json
from turtle import update
from urllib.request import Request
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from driver.models import Driver, DriverOrders
from driver.selectors import find_nearest_driver
from driver.serializers import DriverOrderSerializer, DriverSerializer
from order.serializers import OrderSerializer
import datetime
import requests

from order.models import Order


class DriverViewSet(ModelViewSet):
    @action(detail=False, methods=["get"])
    def nearlocation(self, request):
        date = request.query_params.get("date")
        hour = request.query_params.get("hour")
        lattitude = float(request.query_params.get("lattitude"))
        length = float(request.query_params.get("length"))
        drivers = Driver.objects.filter(updated_at__date=date, updated_at__hour=hour)
        driver_id, distance = find_nearest_driver(drivers, lattitude, length)
        return Response((driver_id, distance), status=status.HTTP_200_OK)

    def create(self, request):
        serializer = DriverSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request):
        #The link should point to the json
        update_drivers: Request = requests.get(
            "https://gist.githubusercontent.com/jeithc/96681e4ac7e2b99cfe9a08ebc093787c/raw/632ca4fc3ffe77b558f467beee66f10470649bb4/points.json"
        )
        if update_drivers.status_code == status.HTTP_200_OK:
            update_drivers = update_drivers.json()["alfreds"]
            for update_driver in update_drivers:
                id_ = update_driver["id"]
                lat = update_driver["lat"]
                lng = update_driver["lng"]
                last_update = update_driver["lastUpdate"]
                Driver.objects.filter(id=id_).update(
                    length_driver=float(lng),
                    latitude_driver=float(lat),
                    updated_at=last_update,
                )
            return Response(status=status.HTTP_200_OK)


class DriverOrderViewSet(ModelViewSet):

    queryset = DriverOrders.objects.all()
    serializer_class = DriverOrderSerializer

    def list(self, request):
        day = request.query_params.get("day")
        driver = request.query_params.get("driver")
        if day and driver is None:
            orders_in_day = DriverOrders.objects.filter(assigned_at__day=day).order_by(
                "assigned_at__hour"
            )
            return Response(
                self.serializer_class(orders_in_day, many=True).data,
                status=status.HTTP_200_OK,
            )
        elif day and driver:
            orders_by_driver_in_day = DriverOrders.objects.filter(
                assigned_at__day=day, driver=driver
            ).order_by("assigned_at__hour")
            return Response(
                self.serializer_class(orders_by_driver_in_day, many=True).data,
                status=status.HTTP_200_OK,
            )
        return Response(
            self.serializer_class(DriverOrders.objects.all(), many=True).data,
            status=status.HTTP_200_OK,
        )

    def update(self, request, pk):
        driver = Driver.objects.get(id=pk)
        if driver.free == True:
            driver.free = False
            driver.save()
            parameters = dict(request.data)
            # This change in parameters is because APIView is changing the information of the body
            parameters = {k: v[0] for k, v in parameters.items()}
            order = Order.objects.create(**parameters)
            DriverOrders.objects.create(
                driver=driver,
                order=order,
                assigned_at=datetime.datetime.now(),
                active=True,
            )
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
