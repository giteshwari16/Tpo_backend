from django.apps import AppConfig


class BackendProjectConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend_project'

    def ready(self):
        """
        Configure admin site branding when app is ready
        """
        from django.contrib import admin
        
        # Customize admin site branding for IMRD
        admin.site.site_title = 'IMRD TPO Admin Panel'
        admin.site.site_header = 'IMRD Training & Placement Office'
        admin.site.index_title = 'Welcome to IMRD TPO Administration'
