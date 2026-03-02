from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes, parser_classes
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from django.db import IntegrityError
from .models import JobProfile, PrepMaterial, FatigueData, User, StudentProfile, JobApplication, Training, TrainingRegistration, ResumeAnalysis
from .ml import loader as ml_loader
from .serializers import JobProfileSerializer, PrepMaterialSerializer, FatigueDataSerializer, StudentProfileSerializer, JobApplicationSerializer, TrainingSerializer, TrainingRegistrationSerializer, ResumeAnalysisSerializer
from services import fetch_external_aptitude, clear_aptitude_cache
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'role')

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def current_user(request):
    """Get current user information"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

class ReadOnlyOrAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

class JobProfileViewSet(viewsets.ModelViewSet):
    queryset = JobProfile.objects.order_by('-created_at')
    serializer_class = JobProfileSerializer
    permission_classes = [ReadOnlyOrAuthenticated]

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def apply(self, request, pk=None):
        # In a real app, create an application record; here we return success.
        job = get_object_or_404(JobProfile, pk=pk)
        return Response({"message": f"Applied to {job.company_name} - {job.role}"})

class PrepMaterialViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PrepMaterial.objects.all().order_by('-created_at')
    serializer_class = PrepMaterialSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        cat = self.request.query_params.get('category')
        if cat:
            qs = qs.filter(category=cat)
        return qs

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def fatigue_analyze(request):
    data = request.data
    try:
        study = float(data.get('study_hours', 0))
        breaks = int(data.get('breaks', 0))
        sleep = float(data.get('sleep_duration', 0))
        load = int(data.get('mental_load', 0))
    except (TypeError, ValueError):
        return Response({"detail":"Invalid input"}, status=status.HTTP_400_BAD_REQUEST)

    # Try ML model first (if trained), mapping wellness inputs to model feature space
    model, meta = ml_loader.get_model()
    predicted_level = None
    if model and meta:
        def clamp(v, lo=0.0, hi=10.0):
            return max(lo, min(hi, float(v)))
        # Optional UI extras
        social_media_hours = float(data.get('social_media_hours', 0))  # expected 0..5
        meals_quality = float(data.get('meals_quality', 3))            # expected 1..5
        productivity_self = float(data.get('productivity_self', 5))    # expected 0..10

        # Feature engineering to the dataset's five scores
        sleep_score = clamp((sleep / 8.0) * 10.0)       # 8h -> 10
        study_score = clamp((study / 10.0) * 10.0)      # 10h -> 10
        social_media_score = clamp((social_media_hours / 5.0) * 10.0)  # 5h -> 10
        meals_score = clamp((meals_quality / 5.0) * 10.0)              # 5 -> 10
        productivity_score_clean = clamp(productivity_self)             # already 0..10

        payload = {
            'sleep_score': sleep_score,
            'study_score': study_score,
            'social_media_score': social_media_score,
            'meals_score': meals_score,
            'productivity_score_clean': productivity_score_clean,
        }
        predicted_level = ml_loader.predict(payload)

    if predicted_level:
        # Normalize label variants
        norm = str(predicted_level).strip().lower()
        if 'high' in norm: level = 'High'
        elif 'medium' in norm: level = 'Medium'
        else: level = 'Low'
        score = 8 if level == 'High' else 5 if level == 'Medium' else 2
        advice = (
            'High Fatigue: 20min nap and reduce screen time.' if level == 'High' else
            'Moderate fatigue: Mix lighter tasks and short breaks.' if level == 'Medium' else
            'Low fatigue: Proceed with focused Coding/DSA blocks.'
        )
    else:
        # Heuristic logic fallback
        if sleep < 6 and study > 8:
            level, score, advice = 'High', 8, 'High Fatigue Detected: 20min power nap, light revision for 1 hour.'
        elif sleep > 7 and breaks > 3:
            level, score, advice = 'Low', 2, 'Low fatigue: Proceed with focused Coding/DSA blocks.'
        else:
            score_val = (study * 1.2) - (sleep * 1.5) - (breaks * 0.5) + (load * 0.6)
            score_val = max(0, min(10, round(score_val)))
            if score_val > 7:
                level, score, advice = 'High', 8, 'Prioritize rest. Limit to light reading today.'
            elif score_val > 4:
                level, score, advice = 'Medium', 5, 'Moderate load: Mix Aptitude and light Tech; avoid heavy coding sprints.'
            else:
                level, score, advice = 'Low', 2, 'Great zone: Schedule deep work on Coding/Projects.'

    # store log
    FatigueData.objects.create(
        user=request.user,
        study_hours=study,
        sleep_duration=sleep,
        breaks=breaks,
        fatigue_score=score,
    )

    return Response({
        "level": level,
        "score": score,
        "advice": advice
    })

@api_view(['GET', 'POST', 'PUT'])
@permission_classes([permissions.IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def profile(request):
    # Ensure a profile exists
    profile, _ = StudentProfile.objects.get_or_create(user=request.user)

    if request.method == 'GET':
        ser = StudentProfileSerializer(profile)
        return Response(ser.data)

    # Accept JSON or multipart for resume upload
    data = request.data.copy()
    # Only allow specific fields to be updated by the student
    allowed_keys = ['branch', 'cgpa', 'skills', 'placement_status', 'phone', 'address', 'graduation_year', 'backlogs', 'internships', 'projects']
    allowed = {k: v for k, v in data.items() if k in allowed_keys}
    files = {}
    if 'resume' in request.FILES:
        files['resume'] = request.FILES['resume']

    ser = StudentProfileSerializer(profile, data={**allowed, **files}, partial=True)
    if ser.is_valid():
        ser.save()
        return Response(ser.data)
    return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_student(request):
    """
    Simple registration endpoint for student users.
    Expects: name, email, password
    """
    name = (request.data.get('name') or "").strip()
    email = (request.data.get('email') or "").strip().lower()
    password = request.data.get('password') or ""

    if not name or not email or not password:
        return Response(
            {"detail": "Name, email and password are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        user = User.objects.create_user(email=email, password=password, role="student")
    except IntegrityError:
        return Response(
            {"detail": "An account with this email already exists."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Split name into first/last (best-effort)
    parts = name.split()
    if parts:
        user.first_name = parts[0]
        if len(parts) > 1:
            user.last_name = " ".join(parts[1:])
        user.save(update_fields=["first_name", "last_name"])

    # Create an empty StudentProfile for the new user
    StudentProfile.objects.get_or_create(user=user)

    return Response(
        {"detail": "Registration successful. You can now log in."},
        status=status.HTTP_201_CREATED,
    )

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def fatigue_data(request):
    """Get user's fatigue data history"""
    data = FatigueData.objects.filter(user=request.user).order_by('-created_at')[:10]
    serializer = FatigueDataSerializer(data, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
@permission_classes([permissions.AllowAny])
def external_aptitude(request):
    """
    API endpoint to fetch external aptitude questions.
    GET: Returns cached questions or fetches fresh ones
    POST: Clears cache and fetches fresh questions (refresh functionality)
    """
    force_refresh = request.method == 'POST'
    
    # Fetch questions from external sources
    result = fetch_external_aptitude(force_refresh=force_refresh)
    
    if result['success']:
        return Response({
            'success': True,
            'questions': result['data'],
            'source': result['source'],
            'message': result['message'],
            'count': len(result['data'])
        })
    else:
        return Response({
            'success': False,
            'questions': [],
            'source': result['source'],
            'message': result['message'],
            'count': 0
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def trainings(request):
    """
    GET: List all available trainings
    POST: Register for a training (students only)
    """
    if request.method == 'GET':
        trainings = Training.objects.filter(is_active=True).order_by('start_date')
        serializer = TrainingSerializer(trainings, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        training_id = request.data.get('training_id')
        if not training_id:
            return Response(
                {"detail": "Training ID is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            training = Training.objects.get(id=training_id, is_active=True)
        except Training.DoesNotExist:
            return Response(
                {"detail": "Training not found or inactive."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if already registered
        if TrainingRegistration.objects.filter(user=request.user, training=training).exists():
            return Response(
                {"detail": "You have already registered for this training."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if training is full
        if training.is_full:
            return Response(
                {"detail": "This training is already full."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create registration
        registration = TrainingRegistration.objects.create(
            user=request.user,
            training=training,
            notes=request.data.get('notes', '')
        )
        
        # Update registered count
        training.registered_count += 1
        training.save()
        
        serializer = TrainingRegistrationSerializer(registration)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_trainings(request):
    """
    Get user's training registrations
    """
    registrations = TrainingRegistration.objects.filter(user=request.user).select_related('training').order_by('-registered_at')
    serializer = TrainingRegistrationSerializer(registrations, many=True)
    return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def training_registration_detail(request, registration_id):
    """
    GET: Get registration details
    PUT: Update registration (notes, feedback, status)
    DELETE: Cancel registration
    """
    try:
        registration = TrainingRegistration.objects.get(
            id=registration_id, 
            user=request.user
        )
    except TrainingRegistration.DoesNotExist:
        return Response(
            {"detail": "Registration not found."},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if request.method == 'GET':
        serializer = TrainingRegistrationSerializer(registration)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        # Allow updating notes, feedback, and status (for cancellation)
        allowed_fields = ['notes', 'feedback']
        if request.data.get('status') in ['cancelled', 'attended', 'completed']:
            allowed_fields.append('status')
        
        for field in allowed_fields:
            if field in request.data:
                setattr(registration, field, request.data[field])
        
        registration.save()
        serializer = TrainingRegistrationSerializer(registration)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        # Update training registered count
        training = registration.training
        training.registered_count = max(0, training.registered_count - 1)
        training.save()
        
        registration.delete()
        return Response(
            {"detail": "Registration cancelled successfully."},
            status=status.HTTP_204_NO_CONTENT
        )

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def resume_analysis(request):
    """
    GET: List user's resume analyses
    POST: Upload and analyze a new resume
    """
    if request.method == 'GET':
        analyses = ResumeAnalysis.objects.filter(user=request.user).order_by('-analysis_date')
        serializer = ResumeAnalysisSerializer(analyses, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        if 'resume_file' not in request.FILES:
            return Response(
                {"detail": "Resume file is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        resume_file = request.FILES['resume_file']
        
        # Validate file type
        allowed_types = ['.pdf', '.doc', '.docx', '.txt']
        file_extension = resume_file.name.lower().split('.')[-1]
        if f'.{file_extension}' not in allowed_types:
            return Response(
                {"detail": f"File type .{file_extension} is not allowed. Allowed types: {', '.join(allowed_types)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate file size (max 5MB)
        if resume_file.size > 5 * 1024 * 1024:
            return Response(
                {"detail": "File size must be less than 5MB"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create analysis record with default values
        try:
            analysis = ResumeAnalysis.objects.create(
                user=request.user,
                resume_file=resume_file,
                overall_score=5,
                ats_score=5,
                structure_score=5,
                content_score=5,
                skills_match=5,
                experience_score=5,
                strengths="Resume uploaded successfully",
                weaknesses="Analysis pending",
                suggestions="Please check back later for detailed analysis",
                key_skills_found="Basic skills detected",
                missing_skills="Advanced skills may be missing"
            )
            
            serializer = ResumeAnalysisSerializer(analysis)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {"detail": f"Error creating analysis: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def resume_analysis_detail(request, analysis_id):
    """
    GET: Get analysis details
    PUT: Update analysis notes
    DELETE: Delete analysis
    """
    try:
        analysis = ResumeAnalysis.objects.get(
            id=analysis_id, 
            user=request.user
        )
    except ResumeAnalysis.DoesNotExist:
        return Response(
            {"detail": "Analysis not found."},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if request.method == 'GET':
        serializer = ResumeAnalysisSerializer(analysis)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        # Allow updating notes and suggestions
        allowed_fields = ['suggestions']
        for field in allowed_fields:
            if field in request.data:
                setattr(analysis, field, request.data[field])
        
        analysis.save()
        serializer = ResumeAnalysisSerializer(analysis)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        # Delete resume file and analysis
        if analysis.resume_file:
            analysis.resume_file.delete()
        analysis.delete()
        return Response(
            {"detail": "Analysis deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )

def simulate_resume_analysis(analysis):
    """
    Simulate resume analysis with mock scoring
    In production, this would use NLP/ML models for real analysis
    """
    import random
    
    # Simulate ATS score (Applicant Tracking System compatibility)
    ats_score = random.randint(4, 9)
    
    # Simulate structure score
    structure_score = random.randint(5, 8)
    
    # Simulate content score
    content_score = random.randint(4, 8)
    
    # Simulate skills matching
    skills_match = random.randint(3, 7)
    
    # Simulate experience score
    experience_score = random.randint(4, 8)
    
    # Calculate overall score (average of all scores)
    overall_score = int((ats_score + structure_score + content_score + skills_match + experience_score) / 5)
    
    # Generate analysis text based on scores
    if overall_score >= 8:
        strengths = "Strong technical skills, good project experience, clear career objectives"
        weaknesses = "Could add more quantifiable achievements"
        suggestions = "Consider adding metrics to showcase impact, highlight leadership experiences"
        key_skills_found = "Python, JavaScript, React, Node.js, SQL, Git"
        missing_skills = "Cloud computing experience, advanced certifications"
    elif overall_score >= 6:
        strengths = "Good technical foundation, some project work"
        weaknesses = "Limited leadership experience, needs more quantifiable results"
        suggestions = "Add more technical projects, consider contributing to open source"
        key_skills_found = "Python, Java, HTML, CSS, basic SQL"
        missing_skills = "Advanced frameworks, cloud platforms, DevOps tools"
    else:
        strengths = "Educational background present"
        weaknesses = "Lacks practical experience, needs skill development"
        suggestions = "Focus on building projects, get internships, learn in-demand technologies"
        key_skills_found = "Basic programming concepts, theoretical knowledge"
        missing_skills = "Practical coding experience, industry-relevant skills"
    
    # Update analysis with simulated results
    analysis.ats_score = ats_score
    analysis.structure_score = structure_score
    analysis.content_score = content_score
    analysis.skills_match = skills_match
    analysis.experience_score = experience_score
    analysis.overall_score = overall_score
    analysis.strengths = strengths
    analysis.weaknesses = weaknesses
    analysis.suggestions = suggestions
    analysis.key_skills_found = key_skills_found
    analysis.missing_skills = missing_skills
    analysis.save()

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def job_applications(request):
    """
    GET: List all applications for current user
    POST: Create new job application
    """
    if request.method == 'GET':
        applications = JobApplication.objects.filter(user=request.user).select_related('job').order_by('-applied_at')
        serializer = JobApplicationSerializer(applications, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        job_id = request.data.get('job_id')
        if not job_id:
            return Response(
                {"detail": "Job ID is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            job = JobProfile.objects.get(id=job_id, is_active=True)
        except JobProfile.DoesNotExist:
            return Response(
                {"detail": "Job not found or inactive."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if already applied
        if JobApplication.objects.filter(user=request.user, job=job).exists():
            return Response(
                {"detail": "You have already applied to this job."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create application
        application = JobApplication.objects.create(
            user=request.user,
            job=job,
            cover_letter=request.data.get('cover_letter', ''),
            notes=request.data.get('notes', '')
        )
        
        # Handle resume upload
        if 'resume' in request.FILES:
            application.resume = request.FILES['resume']
            application.save()
        
        serializer = JobApplicationSerializer(application)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def application_detail(request, application_id):
    """
    GET: Get application details
    PUT: Update application (notes, cover_letter, withdraw)
    DELETE: Delete application
    """
    try:
        application = JobApplication.objects.get(
            id=application_id, 
            user=request.user
        )
    except JobApplication.DoesNotExist:
        return Response(
            {"detail": "Application not found."},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if request.method == 'GET':
        serializer = JobApplicationSerializer(application)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        # Allow updating notes, cover_letter, and status (for withdrawal)
        allowed_fields = ['notes', 'cover_letter']
        if request.data.get('status') == 'withdrawn':
            allowed_fields.append('status')
        
        for field in allowed_fields:
            if field in request.data:
                setattr(application, field, request.data[field])
        
        application.save()
        serializer = JobApplicationSerializer(application)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        application.delete()
        return Response(
            {"detail": "Application deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )
