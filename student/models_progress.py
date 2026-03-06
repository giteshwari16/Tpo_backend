from django.db import models
from django.conf import settings

class StudentProgress(models.Model):
    """Track student progress across different placement preparation activities"""
    
    PROGRESS_CATEGORIES = [
        ('profile', 'Profile Completion'),
        ('aptitude', 'Aptitude Preparation'),
        ('technical', 'Technical Skills'),
        ('interview', 'Interview Preparation'),
        ('resume', 'Resume Building'),
        ('applications', 'Job Applications'),
        ('trainings', 'Training Programs'),
        ('wellness', 'Wellness Activities'),
    ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=PROGRESS_CATEGORIES)
    progress_percentage = models.IntegerField(default=0, help_text="Progress percentage (0-100)")
    last_updated = models.DateTimeField(auto_now=True)
    completed_items = models.JSONField(default=dict, help_text="Track completed items in each category")
    total_items = models.JSONField(default=dict, help_text="Track total items in each category")
    
    class Meta:
        unique_together = ['user', 'category']
    
    def __str__(self):
        return f"{self.user.email} - {self.get_category_display()}: {self.progress_percentage}%"

class ProgressActivity(models.Model):
    """Track individual activities and milestones"""
    
    ACTIVITY_TYPES = [
        ('profile_update', 'Profile Updated'),
        ('aptitude_test', 'Aptitude Test Completed'),
        ('technical_problem', 'Technical Problem Solved'),
        ('interview_practice', 'Interview Practice Session'),
        ('resume_upload', 'Resume Uploaded'),
        ('job_application', 'Job Application Submitted'),
        ('training_registered', 'Training Registered'),
        ('wellness_check', 'Wellness Check-in'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    description = models.TextField()
    points_earned = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict, help_text="Additional activity data")
    
    def __str__(self):
        return f"{self.user.email} - {self.get_activity_type_display()}: {self.points_earned} points"
