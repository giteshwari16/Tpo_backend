from django.apps import AppConfig


class BackendProjectConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend_project'

    def ready(self):
        """
        Keep default Django admin appearance
        """
        # No custom admin configuration - keep Django default
        pass
