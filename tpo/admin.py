from django.contrib import admin
from .models import User, StudentProfile, JobProfile, JobApplication, Training, TrainingRegistration, ResumeAnalysis, PrepMaterial, FatigueData
from backend_project.admin import tpo_admin_site


@tpo_admin_site.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "role", "is_active", "is_staff")
    search_fields = ("email",)
    list_filter = ("role", "is_active", "is_staff")


@tpo_admin_site.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "branch", "cgpa", "placement_status")
    search_fields = ("user__email", "branch")
    list_filter = ("branch", "placement_status")


@tpo_admin_site.register(JobProfile)
class JobProfileAdmin(admin.ModelAdmin):
    list_display = ("company_name", "role", "category", "ctc", "eligibility", "location", "deadline", "is_active", "created_at")
    search_fields = ("company_name", "role", "location", "eligibility", "description")
    list_filter = ("category", "location", "is_active", "created_at", "deadline")
    ordering = ("-created_at",)
    list_editable = ("deadline", "is_active")
    readonly_fields = ("created_at",)
    
    fieldsets = (
        ("Job Information", {
            "fields": ("company_name", "role", "category", "ctc", "eligibility")
        }),
        ("Location & Timeline", {
            "fields": ("location", "deadline", "is_active")
        }),
        ("Description", {
            "fields": ("description",),
            "classes": ("collapse",)
        }),
        ("System Information", {
            "fields": ("created_at",),
            "classes": ("collapse",)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by("-created_at")


@tpo_admin_site.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ("user", "job", "status", "applied_at", "updated_at")
    search_fields = ("user__email", "job__company_name", "job__role")
    list_filter = ("status", "applied_at", "updated_at")
    ordering = ("-applied_at",)
    readonly_fields = ("applied_at", "updated_at")
    
    fieldsets = (
        ("Application Details", {
            "fields": ("user", "job", "status")
        }),
        ("Documents", {
            "fields": ("resume", "cover_letter")
        }),
        ("Notes", {
            "fields": ("notes",),
            "classes": ("collapse",)
        }),
        ("Timestamps", {
            "fields": ("applied_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'job').order_by("-applied_at")


@tpo_admin_site.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ("title", "training_type", "instructor", "start_date", "end_date", "capacity", "registered_count", "is_active")
    search_fields = ("title", "instructor", "venue", "description")
    list_filter = ("training_type", "is_active", "is_online", "start_date")
    ordering = ("-start_date",)
    list_editable = ("is_active", "capacity")
    readonly_fields = ("registered_count", "created_at", "updated_at")
    
    fieldsets = (
        ("Training Information", {
            "fields": ("title", "training_type", "instructor", "description")
        }),
        ("Schedule & Location", {
            "fields": ("start_date", "end_date", "duration_hours", "venue", "is_online")
        }),
        ("Online Details", {
            "fields": ("meeting_link",),
            "classes": ("collapse",)
        }),
        ("Capacity & Registration", {
            "fields": ("capacity", "registered_count", "is_active")
        }),
        ("Learning Details", {
            "fields": ("prerequisites", "learning_outcomes"),
            "classes": ("collapse",)
        }),
        ("System Information", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('registrations').order_by("-start_date")

@tpo_admin_site.register(TrainingRegistration)
class TrainingRegistrationAdmin(admin.ModelAdmin):
    list_display = ("user", "training", "status", "registered_at", "updated_at")
    search_fields = ("user__email", "training__title", "notes")
    list_filter = ("status", "registered_at", "training__training_type")
    ordering = ("-registered_at",)
    readonly_fields = ("registered_at", "updated_at")
    
    fieldsets = (
        ("Registration Details", {
            "fields": ("user", "training", "status")
        }),
        ("Student Information", {
            "fields": ("notes", "feedback"),
            "classes": ("collapse",)
        }),
        ("Timestamps", {
            "fields": ("registered_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'training').order_by("-registered_at")


@tpo_admin_site.register(ResumeAnalysis)
class ResumeAnalysisAdmin(admin.ModelAdmin):
    list_display = ("user", "overall_score", "grade", "ats_score", "analysis_date")
    search_fields = ("user__email", "strengths", "weaknesses", "key_skills_found")
    list_filter = ("overall_score", "analysis_date")
    ordering = ("-analysis_date",)
    readonly_fields = ("analysis_date", "updated_at")
    
    fieldsets = (
        ("Analysis Results", {
            "fields": ("user", "overall_score", "grade", "ats_score")
        }),
        ("Detailed Scores", {
            "fields": ("structure_score", "content_score", "skills_match", "experience_score")
        }),
        ("Analysis Details", {
            "fields": ("strengths", "weaknesses", "suggestions")
        }),
        ("Skills Analysis", {
            "fields": ("key_skills_found", "missing_skills")
        }),
        ("Documents", {
            "fields": ("resume_file",)
        }),
        ("Metadata", {
            "fields": ("analysis_date", "updated_at"),
            "classes": ("collapse",)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user').order_by("-analysis_date")


@tpo_admin_site.register(PrepMaterial)
class PrepMaterialAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "created_at")
    search_fields = ("title", "category")
    list_filter = ("category",)
    ordering = ("-created_at",)


@tpo_admin_site.register(FatigueData)
class FatigueDataAdmin(admin.ModelAdmin):
    list_display = ("user", "study_hours", "sleep_duration", "breaks", "fatigue_score", "timestamp")
    search_fields = ("user__email",)
    list_filter = ("timestamp",)
    ordering = ("-timestamp",)

