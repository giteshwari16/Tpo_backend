from django.contrib import admin
from .models import PlacementProfile
from backend_project.admin import tpo_admin_site

@tpo_admin_site.register(PlacementProfile)
class PlacementProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "department", "cgpa", "backlogs", "year")
    list_filter = ("department", "backlogs", "trainings_attended", "year")
    search_fields = ("user__username", "roll_number", "department")
