from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from .asgi import get_asgi_application
import chat.routing
from chat.channelsmiddleware import JWTAuthMiddlewareStack

application = ProtocolTypeRouter({
    'websocket': JWTAuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
