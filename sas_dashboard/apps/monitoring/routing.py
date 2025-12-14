from django.urls import path, re_path
from .consumers import MonitoringConsumer, LiveFeedConsumer

websocket_urlpatterns = [
    path("ws/monitoring/", MonitoringConsumer.as_asgi()),
    re_path(r"ws/live-feed/$", LiveFeedConsumer.as_asgi()),
]