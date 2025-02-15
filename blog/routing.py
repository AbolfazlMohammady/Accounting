from django.urls import re_path
from .consumers import PostViewConsumer

websocket_urlpatterns = [
    re_path(r"ws/posts/(?P<post_id>\d+)/$", PostViewConsumer.as_asgi()),
]
