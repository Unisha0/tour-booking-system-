# tour/apps.py
from django.apps import AppConfig

class TourConfig(AppConfig):
    name = 'tour'

    def ready(self):
        # Signals are intentionally not imported; we avoid automatic DB side-effects.
        pass