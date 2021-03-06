from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path, include, re_path
from django.conf.urls import url
from chat.consumers import ChatConsumer

ws_urlpatterns = [
    re_path(r'^ws/(?P<room_id>\w+)/$', ChatConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            ws_urlpatterns
        )
    )
})