from django.apps import AppConfig


class PackageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'package'

    def ready(self):
        import package.signals

