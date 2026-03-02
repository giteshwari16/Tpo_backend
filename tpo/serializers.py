from rest_framework import serializers
from .models import User, StudentProfile, JobProfile, JobApplication, Training, TrainingRegistration, ResumeAnalysis, PrepMaterial, FatigueData

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "role"]

class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = StudentProfile
        fields = [
            "id", "user", "branch", "cgpa", "skills",
            "phone", "address", "graduation_year", "backlogs", "internships", "projects",
            "resume", "placement_status"
        ]

class JobProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobProfile
        fields = [
            "id", "company_name", "role", "category", "ctc", "eligibility", 
            "location", "deadline", "description", "is_active", "created_at"
        ]

class JobApplicationSerializer(serializers.ModelSerializer):
    job = JobProfileSerializer(read_only=True)
    
    class Meta:
        model = JobApplication
        fields = [
            "id", "job", "status", "applied_at", "updated_at", 
            "resume", "cover_letter", "notes"
        ]
        read_only_fields = ["applied_at", "updated_at"]

class TrainingSerializer(serializers.ModelSerializer):
    registrations_count = serializers.SerializerMethodField()
    spots_available = serializers.SerializerMethodField()
    is_full = serializers.SerializerMethodField()
    
    class Meta:
        model = Training
        fields = [
            "id", "title", "description", "training_type", "instructor", "venue",
            "start_date", "end_date", "duration_hours", "capacity", "registered_count",
            "is_active", "is_online", "meeting_link", "prerequisites", 
            "learning_outcomes", "created_at", "updated_at",
            "registrations_count", "spots_available", "is_full"
        ]
        read_only_fields = ["registered_count", "created_at", "updated_at"]
    
    def get_registrations_count(self, obj):
        return obj.registrations.count()
    
    def get_spots_available(self, obj):
        return max(0, obj.capacity - obj.registered_count)
    
    def get_is_full(self, obj):
        return obj.registered_count >= obj.capacity

class TrainingRegistrationSerializer(serializers.ModelSerializer):
    training = TrainingSerializer(read_only=True)
    
    class Meta:
        model = TrainingRegistration
        fields = [
            "id", "training", "status", "registered_at", "updated_at", 
            "notes", "feedback"
        ]
        read_only_fields = ["registered_at", "updated_at"]

class ResumeAnalysisSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = ResumeAnalysis
        fields = [
            "id", "user", "resume_file", "overall_score", "grade", "ats_score",
            "structure_score", "content_score", "skills_match", "experience_score",
            "strengths", "weaknesses", "suggestions", 
            "key_skills_found", "missing_skills", "analysis_date", "updated_at"
        ]
        read_only_fields = ["analysis_date", "updated_at"]

class PrepMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrepMaterial
        fields = ["id", "title", "content", "category", "created_at"]

class FatigueDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FatigueData
        fields = ["id", "study_hours", "sleep_duration", "breaks", "fatigue_score", "timestamp"]
