from django.urls import path
from . import views_progress

urlpatterns = [
    path('progress/summary/', views_progress.progress_summary, name='progress_summary'),
    path('progress/update/', views_progress.update_progress, name='update_progress'),
    path('progress/activities/', views_progress.progress_activities, name='progress_activities'),
]
