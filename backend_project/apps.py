from django.apps import AppConfig


class BackendProjectConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend_project'

    def ready(self):
        """
        Configure admin site branding when app is ready
        """
        from django.contrib import admin
        
        # Customize admin site branding
        admin.site.site_title = 'TPO Admin Panel'
        admin.site.site_header = 'TPO Administration'
        admin.site.index_title = 'Welcome to TPO Admin Portal'
