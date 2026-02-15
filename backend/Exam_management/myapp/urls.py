from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    register_view, login_view, profile_view, profile_update_view,
    dashboard_view,
    StudentViewSet, StaffViewSet, DepartmentViewSet, CourseViewSet,
    ExamViewSet, ExamScheduleViewSet, HallTicketViewSet,
    MarksEntryViewSet, ResultViewSet, NotificationViewSet
)

# Create router and register viewsets
router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='student')
router.register(r'staff', StaffViewSet, basename='staff')
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'exams', ExamViewSet, basename='exam')
router.register(r'exam-schedules', ExamScheduleViewSet, basename='exam-schedule')
router.register(r'hall-tickets', HallTicketViewSet, basename='hall-ticket')
router.register(r'marks', MarksEntryViewSet, basename='marks')
router.register(r'results', ResultViewSet, basename='result')
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    # Authentication URLs
    path('auth/register/', register_view, name='register'),
    path('auth/login/', login_view, name='login'),
    path('auth/profile/', profile_view, name='profile'),
    path('auth/profile/update/', profile_update_view, name='profile-update'),
    
    # Dashboard URL
    path('dashboard/', dashboard_view, name='dashboard'),
    
    # Include router URLs
    path('', include(router.urls)),
]
