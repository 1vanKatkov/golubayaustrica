"""ASGI entry point for poker_site."""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "poker_site.settings")

application = get_asgi_application()

