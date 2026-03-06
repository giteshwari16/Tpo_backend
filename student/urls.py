from django.urls import path
from .views import MePlacementProfile, OnboardingStatus
from . import urls_progress

urlpatterns = [
    path('me/', MePlacementProfile.as_view(), name='student_me_profile'),
    path('onboarding-status/', OnboardingStatus.as_view(), name='student_onboarding_status'),
]

# Add progress tracking URLs
urlpatterns += urls_progress.urlpatterns
