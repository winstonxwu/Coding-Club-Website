from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MemberViewSet, register, MeetingViewSet, current_user, AttendanceViewSet, students_list

router = DefaultRouter()
router.register(r'members', MemberViewSet)
router.register(r'meetings', MeetingViewSet)
router.register(r'attendance', AttendanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', register, name='register'),
    path('current-user/', current_user, name='current-user'),
    path('students-list/', students_list, name='students-list'),
]