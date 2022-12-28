import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import path


import eshop.routing
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eshop.settings")
django_asgi_app = get_asgi_application()


django_asgi_app = get_asgi_application()
from Accounts.models import *
application = ProtocolTypeRouter({
   # Django's ASGI application to handle traditional HTTP requests
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
             URLRouter(
            eshop.routing.websocket_urlpatterns
        )
        )
    ),

})