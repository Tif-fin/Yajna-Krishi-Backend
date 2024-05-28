from django.apps import AppConfig


class AuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Auth'
    def ready(self):
        import Auth.Schedule.updater as updater
        updater.start()

