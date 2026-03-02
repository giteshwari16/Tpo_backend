from django.db import models
from django.conf import settings

class PlacementProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Personal Details
    roll_number = models.CharField(max_length=20, blank=True, null=True)
    department = models.CharField(max_length=50, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    # Academic Details
    tenth_percentage = models.FloatField(blank=True, null=True)
    twelfth_percentage = models.FloatField(blank=True, null=True)
    cgpa = models.FloatField(blank=True, null=True)
    backlogs = models.BooleanField(default=False)
    num_backlogs = models.IntegerField(default=0)
    # Skills & Technical Profile
    programming_languages = models.TextField(blank=True, null=True)
    core_subjects = models.TextField(blank=True, null=True)
    tools_technologies = models.TextField(blank=True, null=True)
    certifications = models.TextField(blank=True, null=True)
    # Training & Internship
    trainings_attended = models.BooleanField(default=False)
    internship_org = models.CharField(max_length=100, blank=True, null=True)
    internship_duration = models.IntegerField(blank=True, null=True)
    # Placement Preferences
    job_roles = models.TextField(blank=True, null=True)
    preferred_domain = models.CharField(max_length=50, blank=True, null=True)
    relocation = models.BooleanField(default=False)
    # Documents
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    certificates = models.FileField(upload_to='certificates/', blank=True, null=True)

    def __str__(self):
        return f"{getattr(self.user, 'username', str(self.user))} Profile" 
