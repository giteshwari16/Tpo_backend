from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.email} ({self.role})"

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    branch = models.CharField(max_length=50, blank=True)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    skills = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    graduation_year = models.IntegerField(null=True, blank=True)
    backlogs = models.IntegerField(default=0)
    internships = models.TextField(blank=True)
    projects = models.TextField(blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    PLACEMENT_CHOICES = (
        ('placed', 'Placed'),
        ('in_process', 'In Process'),
        ('not_placed', 'Not Placed'),
    )
    placement_status = models.CharField(max_length=20, choices=PLACEMENT_CHOICES, default='not_placed')

    def __str__(self):
        return f"Profile<{self.user.email}>"

class JobProfile(models.Model):
    CATEGORY_CHOICES = (
        ('IT', 'IT Services'),
        ('Product', 'Product Based'),
        ('Core', 'Core Engineering'),
        ('Consulting', 'Consulting'),
        ('Startup', 'Startup'),
        ('Other', 'Other'),
    )
    
    company_name = models.CharField(max_length=120)
    role = models.CharField(max_length=120)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Other')
    ctc = models.CharField(max_length=60)
    eligibility = models.CharField(max_length=120, blank=True)
    location = models.CharField(max_length=120, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    description = models.TextField(blank=True, help_text="Job description and requirements")
    is_active = models.BooleanField(default=True, help_text="Whether this job is currently active")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company_name} - {self.role}"

class JobApplication(models.Model):
    STATUS_CHOICES = (
        ('applied', 'Applied'),
        ('under_review', 'Under Review'),
        ('shortlisted', 'Shortlisted'),
        ('interview_scheduled', 'Interview Scheduled'),
        ('selected', 'Selected'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_applications')
    job = models.ForeignKey(JobProfile, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resume = models.FileField(upload_to='application_resumes/', blank=True, null=True)
    cover_letter = models.TextField(blank=True, help_text="Optional cover letter for the application")
    notes = models.TextField(blank=True, help_text="Personal notes about this application")
    
    class Meta:
        unique_together = ['user', 'job']  # Prevent duplicate applications
    
    def __str__(self):
        return f"{self.user.email} - {self.job.company_name} ({self.status})"

class Training(models.Model):
    TRAINING_TYPE_CHOICES = (
        ('technical', 'Technical Skills'),
        ('soft_skills', 'Soft Skills'),
        ('aptitude', 'Aptitude Training'),
        ('interview', 'Interview Preparation'),
        ('workshop', 'Workshop'),
        ('certification', 'Certification'),
        ('other', 'Other'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField(help_text="Detailed description of the training")
    training_type = models.CharField(max_length=20, choices=TRAINING_TYPE_CHOICES, default='technical')
    instructor = models.CharField(max_length=100, help_text="Trainer/Instructor name")
    venue = models.CharField(max_length=200, help_text="Training location or online platform")
    start_date = models.DateTimeField(help_text="Training start date and time")
    end_date = models.DateTimeField(help_text="Training end date and time")
    duration_hours = models.IntegerField(help_text="Duration in hours")
    capacity = models.IntegerField(help_text="Maximum number of participants")
    registered_count = models.IntegerField(default=0, help_text="Number of registered participants")
    is_active = models.BooleanField(default=True, help_text="Whether registration is open")
    is_online = models.BooleanField(default=False, help_text="Whether this is an online training")
    meeting_link = models.URLField(blank=True, null=True, help_text="Online meeting link for virtual training")
    prerequisites = models.TextField(blank=True, help_text="Required knowledge or skills")
    learning_outcomes = models.TextField(help_text="What participants will learn")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.title} ({self.get_training_type_display()})"
    
    @property
    def is_full(self):
        return self.registered_count >= self.capacity
    
    @property
    def spots_available(self):
        return max(0, self.capacity - self.registered_count)

class TrainingRegistration(models.Model):
    STATUS_CHOICES = (
        ('registered', 'Registered'),
        ('attended', 'Attended'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='training_registrations')
    training = models.ForeignKey(Training, on_delete=models.CASCADE, related_name='registrations')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='registered')
    registered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, help_text="Student notes about the training")
    feedback = models.TextField(blank=True, help_text="Student feedback after completion")
    
    class Meta:
        unique_together = ['user', 'training']  # Prevent duplicate registrations
    
    def __str__(self):
        return f"{self.user.email} - {self.training.title} ({self.status})"

class ResumeAnalysis(models.Model):
    SCORE_CHOICES = (
        (1, 'Very Poor'),
        (2, 'Poor'),
        (3, 'Below Average'),
        (4, 'Average'),
        (5, 'Good'),
        (6, 'Very Good'),
        (7, 'Excellent'),
        (8, 'Outstanding'),
        (9, 'Exceptional'),
        (10, 'Perfect'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resume_analyses')
    resume_file = models.FileField(upload_to='resume_analyses/')
    overall_score = models.IntegerField(choices=SCORE_CHOICES, help_text="Overall resume score (1-10)")
    ats_score = models.IntegerField(choices=SCORE_CHOICES, help_text="Applicant Tracking System score")
    structure_score = models.IntegerField(choices=SCORE_CHOICES, help_text="Resume structure and formatting score")
    content_score = models.IntegerField(choices=SCORE_CHOICES, help_text="Content quality and relevance score")
    skills_match = models.IntegerField(choices=SCORE_CHOICES, help_text="Skills matching score")
    experience_score = models.IntegerField(choices=SCORE_CHOICES, help_text="Experience presentation score")
    
    # Analysis details
    strengths = models.TextField(help_text="Identified strengths in the resume")
    weaknesses = models.TextField(help_text="Areas for improvement")
    suggestions = models.TextField(help_text="Specific suggestions for improvement")
    key_skills_found = models.TextField(help_text="Skills identified from resume analysis")
    missing_skills = models.TextField(help_text="Important skills that are missing")
    
    # Metadata
    analysis_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-analysis_date']
    
    def __str__(self):
        return f"{self.user.email} - Resume Analysis ({self.analysis_date})"
    
    @property
    def grade(self):
        if self.overall_score >= 9:
            return 'A+'
        elif self.overall_score >= 8:
            return 'A'
        elif self.overall_score >= 7:
            return 'B+'
        elif self.overall_score >= 6:
            return 'B'
        elif self.overall_score >= 5:
            return 'C+'
        elif self.overall_score >= 4:
            return 'C'
        else:
            return 'D'

class PrepMaterial(models.Model):
    CATEGORY_CHOICES = (
        ('aptitude', 'Aptitude'),
        ('dbms', 'DBMS'),
        ('os', 'Operating Systems'),
        ('cn', 'Computer Networks'),
        ('coding', 'Coding'),
        ('other', 'Other'),
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} [{self.category}]"

class FatigueData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fatigue_logs')
    study_hours = models.DecimalField(max_digits=4, decimal_places=1)
    sleep_duration = models.DecimalField(max_digits=4, decimal_places=1)
    breaks = models.IntegerField(default=0)
    fatigue_score = models.IntegerField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Fatigue<{self.user.email}> score={self.fatigue_score} at {self.timestamp}"
