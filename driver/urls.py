from django.urls import path

from driver.views import DriverOrderViewSet, DriverViewSet

urlpatterns = [
    path("", DriverViewSet.as_view({"get": "list", "post": "create", "put": "update"})),
    path("nearlocation/", DriverViewSet.as_view({"get": "nearlocation"})),
    path("assing/order/list/", DriverOrderViewSet.as_view({"get": "list"})),
    path("assign/order/<int:pk>/", DriverOrderViewSet.as_view({"put": "update"})),
]
