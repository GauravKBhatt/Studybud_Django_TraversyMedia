"""
ASGI config for studybud project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studybud.settings')

django_asgi_app = get_asgi_application()


from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.security.websocket import AllowedHostOriginValidator
# AllowedHostOriginValidator does not exist in channels.security.websocket from channels 4.0 onwards
from channels.auth import AuthMiddlewareStack
# routing file must be called after calling the application.

from rtchat import routing 

application=ProtocolTypeRouter({
    "http": django_asgi_app,
    # "websocket": AllowedHostOriginValidator(AuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns)))
    
    # AllowedHostOriginValidator only lets those hosts use this web sockets that are declared in settings.py
    #AuthMiddlewareStack helps identify the logged in users.
    #URLRouter helps map the url to correct function in the backend.

    #now if i want to restrict the users to allowed hosts, i will have to do it insode consumers.

    "websocket":AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatters
        )
    )
})