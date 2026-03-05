from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy

class TPOAdminSite(AdminSite):
    """Custom admin site for TPO Portal"""
    site_title = gettext_lazy('TPO Admin Panel')
    site_header = gettext_lazy('TPO Administration')
    index_title = gettext_lazy('Welcome to TPO Admin Portal')

    def get_app_list(self, request):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        app_dict = self._build_app_dict(request)
        
        # Sort the apps alphabetically.
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())
        
        # Move TPO apps to the top
        tpo_apps = []
        other_apps = []
        
        for app in app_list:
            if app['app_label'] in ['tpo', 'student']:
                tpo_apps.append(app)
            else:
                other_apps.append(app)
        
        return tpo_apps + other_apps

# Create custom admin site instance
tpo_admin_site = TPOAdminSite(name='tpo_admin')
