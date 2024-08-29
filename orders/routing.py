from django.urls import re_path

from orders import consumers

websocket_urlpatterns = [
    re_path(r"ws/orders/(?P<location_id>\w+)/$", consumers.OrderConsumer.as_asgi()),
]
