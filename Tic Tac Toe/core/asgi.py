"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from django.urls import path,include
from game.consumers import *
application = get_asgi_application()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myapp.settings')
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket"  : URLRouter([
            path("ws/game/<int:id>/",opponent.as_asgi())

    ]),
})