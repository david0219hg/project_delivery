import math
from driver.models import Driver


def find_nearest_driver(drivers: Driver, lattitude: float, length: float):
    nearest_driver = 0
    minimum_value = 200
    for driver in drivers:
        distance = math.dist(
            [driver.length_driver, driver.latitude_driver], [length, lattitude]
        )
        if  distance < minimum_value:
            minimum_value = distance
            nearest_driver = driver.id

    return nearest_driver, distance
