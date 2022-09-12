import pytest
import datetime
from rest_framework.test import APIClient
from rest_framework import status
from driver.models import Driver, DriverOrders
from driver.factory import DriverFactory, DriverOrderFactory
from order.factory import OrderFactory

from order.models import Order


@pytest.mark.django_db
def test_create_driver():
    ORDER_DATA = {
        "free": True,
        "latitude_driver": 15,
        "length_driver": 15,
        "updated_at": datetime.datetime.now(),
    }
    response = APIClient().post("/driver/", ORDER_DATA, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Driver.objects.all().first().latitude_driver == 15


@pytest.mark.django_db
def test_update_drivers():
    for idx in range(1, 21):
        DriverFactory(id=idx)
    response = APIClient().put("/driver/", format="json")
    assert response.status_code == status.HTTP_200_OK
    assert Driver.objects.get(id=1).latitude_driver == 1
    assert Driver.objects.get(id=2).length_driver == 6


@pytest.mark.django_db
def test_assign_order_to_driver():
    driver = DriverFactory(free=True)
    body = {
        "date_time_arrive": datetime.datetime(2015, 10, 1, 20, 0, 0, 0),
        "date_time_delivery": datetime.datetime(2015, 10, 1, 21, 0, 0, 0),
        "latitude_arrrive": 30,
        "length_arrrive": 30,
        "latitude_delivery": 60,
        "length_delivery": 45,
    }
    response = APIClient().put(f"/driver/assign/order/{driver.id}/", body)
    assert response.status_code == status.HTTP_200_OK
    assert Order.objects.all().first().length_delivery == body["length_delivery"]
    assert DriverOrders.objects.all().first() is not None


@pytest.mark.django_db
def test_get_order_by_day():

    for idx in range(1, 6):
        # assigned same day
        DriverOrderFactory(
            driver=DriverFactory(),
            order=OrderFactory(),
            assigned_at=datetime.datetime(2022, 10, 1, idx, 1, 1, 1),
        )

    # assigned in different day
    DriverOrderFactory(
        driver=DriverFactory(),
        order=OrderFactory(),
        assigned_at=datetime.datetime(2022, 10, 3, 4, 1, 1, 1),
    )

    response = APIClient().get(f"/driver/assing/order/list/?day=1")

    assert response.status_code == status.HTTP_200_OK
    DATE_TIME_RESPONSE = [
        each_response["assigned_at"] for each_response in response.data
    ]

    EXPECTED_RESPONSE = [
        "2022-10-01T01:01:01.000001Z",
        "2022-10-01T02:01:01.000001Z",
        "2022-10-01T03:01:01.000001Z",
        "2022-10-01T04:01:01.000001Z",
        "2022-10-01T05:01:01.000001Z",
    ]

    assert DATE_TIME_RESPONSE == EXPECTED_RESPONSE


@pytest.mark.django_db
def test_get_order_by_driver_and_day():

    driver = DriverFactory()
    for idx in range(1, 6):
        # assigned same day
        DriverOrderFactory(
            driver=driver,
            order=OrderFactory(),
            assigned_at=datetime.datetime(2022, 10, 1, idx, 1, 1, 1),
        )

    # assigned in different day
    DriverOrderFactory(
        driver=DriverFactory(),
        order=OrderFactory(),
        assigned_at=datetime.datetime(2022, 10, 3, 4, 1, 1, 1),
    )

    response = APIClient().get(f"/driver/assing/order/list/?day=1&driver={driver.id}")

    assert response.status_code == status.HTTP_200_OK
    DATE_TIME_RESPONSE = [
        each_response["assigned_at"] for each_response in response.data
    ]

    DRIVER_RESPONSE = [each_response["driver"] for each_response in response.data]

    EXPECTED_TIME_RESPONSE = [
        "2022-10-01T01:01:01.000001Z",
        "2022-10-01T02:01:01.000001Z",
        "2022-10-01T03:01:01.000001Z",
        "2022-10-01T04:01:01.000001Z",
        "2022-10-01T05:01:01.000001Z",
    ]

    EXPECTED_DRIVER_RESPONSE = [driver.id for _ in range(5)]

    assert DATE_TIME_RESPONSE == EXPECTED_TIME_RESPONSE
    assert DRIVER_RESPONSE == EXPECTED_DRIVER_RESPONSE


@pytest.mark.django_db
def test_get_nearest_driver():
    # create and update drivers
    for idx in range(1, 21):
        DriverFactory(id=idx)

    response_update_drivers = APIClient().put("/driver/", format="json")
    assert response_update_drivers.status_code == status.HTTP_200_OK

    response = APIClient().get(
        f"/driver/nearlocation/?lattitude=50&length=50&date=2021-12-10&hour=0"
    )
    assert response.data == (12, 50.99019513592785)
