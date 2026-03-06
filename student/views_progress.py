from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from .models_progress import StudentProgress, ProgressActivity
from .serializers_progress import StudentProgressSerializer, ProgressActivitySerializer, ProgressSummarySerializer
from tpo.models import JobApplication, TrainingRegistration, ResumeAnalysis

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def progress_summary(request):
    """Get comprehensive progress summary for the student"""
    user = request.user
    
    # Get or create progress records for all categories
    progress_data = {}
    for category, _ in StudentProgress.PROGRESS_CATEGORIES:
        progress, created = StudentProgress.objects.get_or_create(
            user=user,
            category=category,
            defaults={'progress_percentage': 0, 'completed_items': {}, 'total_items': {}}
        )
        progress_data[category] = progress
    
    # Calculate actual progress based on user data
    calculate_user_progress(user, progress_data)
    
    # Get recent activities
    recent_activities = ProgressActivity.objects.filter(user=user).order_by('-created_at')[:10]
    
    # Calculate achievements and milestones
    achievements = calculate_achievements(user, progress_data)
    milestones = calculate_next_milestones(user, progress_data)
    
    # Prepare summary data
    summary_data = {
        'total_progress': calculate_overall_progress(progress_data),
        'profile_completion': progress_data['profile'].progress_percentage,
        'aptitude_progress': progress_data['aptitude'].progress_percentage,
        'technical_progress': progress_data['technical'].progress_percentage,
        'interview_progress': progress_data['interview'].progress_percentage,
        'resume_progress': progress_data['resume'].progress_percentage,
        'applications_progress': progress_data['applications'].progress_percentage,
        'trainings_progress': progress_data['trainings'].progress_percentage,
        'wellness_progress': progress_data['wellness'].progress_percentage,
        'recent_activities': ProgressActivitySerializer(recent_activities, many=True).data,
        'achievements': achievements,
        'next_milestones': milestones
    }
    
    serializer = ProgressSummarySerializer(summary_data)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_progress(request):
    """Update progress for a specific category"""
    user = request.user
    category = request.data.get('category')
    completed_item = request.data.get('completed_item')
    
    if category not in dict(StudentProgress.PROGRESS_CATEGORIES):
        return Response(
            {'error': 'Invalid category'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    progress, created = StudentProgress.objects.get_or_create(
        user=user,
        category=category,
        defaults={'progress_percentage': 0, 'completed_items': {}, 'total_items': {}}
    )
    
    # Update completed items
    if completed_item:
        completed_items = progress.completed_items or {}
        completed_items[completed_item] = timezone.now().isoformat()
        progress.completed_items = completed_items
        progress.save()
        
        # Log activity
        activity_type = get_activity_type_for_category(category)
        ProgressActivity.objects.create(
            user=user,
            activity_type=activity_type,
            description=f"Completed {completed_item} in {category}",
            points_earned=10
        )
    
    # Recalculate progress percentage
    calculate_category_progress(progress)
    
    serializer = StudentProgressSerializer(progress)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def progress_activities(request):
    """Get all progress activities for the student"""
    activities = ProgressActivity.objects.filter(user=request.user).order_by('-created_at')
    serializer = ProgressActivitySerializer(activities, many=True)
    return Response(serializer.data)

def calculate_user_progress(user, progress_data):
    """Calculate actual progress based on user's data"""
    try:
        # Profile completion
        from student.models import PlacementProfile
        profile = PlacementProfile.objects.filter(user=user).first()
        if profile:
            profile_fields = ['roll_number', 'department', 'year', 'contact_number', 
                            'tenth_percentage', 'twelfth_percentage', 'cgpa']
            completed = sum(1 for field in profile_fields if getattr(profile, field))
            profile_progress = progress_data['profile']
            profile_progress.progress_percentage = int((completed / len(profile_fields)) * 100)
            profile_progress.save()
        
        # Applications progress
        applications_count = JobApplication.objects.filter(user=user).count()
        applications_progress = progress_data['applications']
        applications_progress.progress_percentage = min(applications_count * 20, 100)  # 20% per application
        applications_progress.save()
        
        # Trainings progress
        trainings_count = TrainingRegistration.objects.filter(user=user).count()
        trainings_progress = progress_data['trainings']
        trainings_progress.progress_percentage = min(trainings_count * 25, 100)  # 25% per training
        trainings_progress.save()
        
        # Resume progress
        resume_count = ResumeAnalysis.objects.filter(user=user).count()
        resume_progress = progress_data['resume']
        resume_progress.progress_percentage = min(resume_count * 50, 100)  # 50% per resume analysis
        resume_progress.save()
        
    except Exception as e:
        print(f"Error calculating progress: {e}")

def calculate_category_progress(progress):
    """Calculate progress percentage for a category"""
    completed_items = progress.completed_items or {}
    total_items = progress.total_items or {}
    
    if not total_items:
        progress.progress_percentage = 0
        return
    
    completed_count = len(completed_items)
    total_count = len(total_items)
    
    if total_count > 0:
        progress.progress_percentage = int((completed_count / total_count) * 100)
    
    progress.save()

def calculate_overall_progress(progress_data):
    """Calculate overall progress across all categories"""
    total_progress = sum(p.progress_percentage for p in progress_data.values())
    return int(total_progress / len(progress_data))

def calculate_achievements(user, progress_data):
    """Calculate user achievements"""
    achievements = []
    
    for category, progress in progress_data.items():
        if progress.progress_percentage >= 100:
            achievements.append(f"Mastered {progress.get_category_display()}")
        elif progress.progress_percentage >= 75:
            achievements.append(f"Advanced {progress.get_category_display()}")
        elif progress.progress_percentage >= 50:
            achievements.append(f"Intermediate {progress.get_category_display()}")
        elif progress.progress_percentage >= 25:
            achievements.append(f"Beginner {progress.get_category_display()}")
    
    return achievements

def calculate_next_milestones(user, progress_data):
    """Calculate next milestones for the user"""
    milestones = []
    
    for category, progress in progress_data.items():
        if progress.progress_percentage < 100:
            next_level = ((progress.progress_percentage // 25) + 1) * 25
            milestones.append(f"Complete {progress.get_category_display()} to {next_level}%")
    
    return milestones[:5]  # Return top 5 milestones

def get_activity_type_for_category(category):
    """Map category to activity type"""
    mapping = {
        'profile': 'profile_update',
        'aptitude': 'aptitude_test',
        'technical': 'technical_problem',
        'interview': 'interview_practice',
        'resume': 'resume_upload',
        'applications': 'job_application',
        'trainings': 'training_registered',
        'wellness': 'wellness_check'
    }
    return mapping.get(category, 'profile_update')
