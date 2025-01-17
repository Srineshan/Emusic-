from django.apps import AppConfig


class EmusicConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'EMusic'
    def ready(self):
        import EMusic.signals

