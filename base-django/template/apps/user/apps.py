from django.apps import AppConfig

class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.user'

    def ready(self):
        import apps.user.allauth_override
        import apps.user.auth.flow_fix
        import apps.user.signals
