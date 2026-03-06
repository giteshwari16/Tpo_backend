from rest_framework import serializers
from .models_progress import StudentProgress, ProgressActivity

class StudentProgressSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = StudentProgress
        fields = ['id', 'category', 'category_display', 'progress_percentage', 
                 'last_updated', 'completed_items', 'total_items']

class ProgressActivitySerializer(serializers.ModelSerializer):
    activity_type_display = serializers.CharField(source='get_activity_type_display', read_only=True)
    
    class Meta:
        model = ProgressActivity
        fields = ['id', 'activity_type', 'activity_type_display', 'description', 
                 'points_earned', 'created_at', 'metadata']

class ProgressSummarySerializer(serializers.Serializer):
    """Serializer for overall progress summary"""
    total_progress = serializers.IntegerField()
    profile_completion = serializers.IntegerField()
    aptitude_progress = serializers.IntegerField()
    technical_progress = serializers.IntegerField()
    interview_progress = serializers.IntegerField()
    resume_progress = serializers.IntegerField()
    applications_progress = serializers.IntegerField()
    trainings_progress = serializers.IntegerField()
    wellness_progress = serializers.IntegerField()
    recent_activities = ProgressActivitySerializer(many=True)
    achievements = serializers.ListField()
    next_milestones = serializers.ListField()
