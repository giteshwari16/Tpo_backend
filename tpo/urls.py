from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import JobProfileViewSet, PrepMaterialViewSet, fatigue_analyze, profile, register_student, external_aptitude, current_user, fatigue_data, job_applications, application_detail, trainings, my_trainings, training_registration_detail, resume_analysis, resume_analysis_detail

router = DefaultRouter()
router.register(r'jobs', JobProfileViewSet, basename='jobs')
router.register(r'prep', PrepMaterialViewSet, basename='prep')

urlpatterns = [
    path('', include(router.urls)),
    path('fatigue/', fatigue_analyze, name='fatigue-analyze'),
    path('fatigue-data/', fatigue_data, name='fatigue-data'),
    path('profile/', profile, name='student-profile'),
    path('register/', register_student, name='student-register'),
    path('external-aptitude/', external_aptitude, name='external-aptitude'),
    path('user/', current_user, name='current-user'),
    path('applications/', job_applications, name='job-applications'),
    path('applications/<int:application_id>/', application_detail, name='application-detail'),
    path('trainings/', trainings, name='trainings'),
    path('my-trainings/', my_trainings, name='my-trainings'),
    path('trainings/<int:registration_id>/', training_registration_detail, name='training-registration-detail'),
    path('resume-analysis/', resume_analysis, name='resume-analysis'),
    path('resume-analysis/<int:analysis_id>/', resume_analysis_detail, name='resume-analysis-detail'),
]
