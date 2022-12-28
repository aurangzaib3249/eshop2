from django.urls import re_path,path

from .consumers import *

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
    path(r'ws/notify/<uuid:room_name>/', Notification.as_asgi()),
    path(r'ws/group/<uuid:room_name>/', GroupChat.as_asgi()),
]