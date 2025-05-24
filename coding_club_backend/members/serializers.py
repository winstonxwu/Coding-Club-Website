from rest_framework import serializers
from .models import Member, Meeting, Attendance

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'email', 'first_name', 'last_name', 'grade', 'account_type', 'date_joined']
        read_only_fields = ['id', 'date_joined']

class MeetingSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = Meeting
        fields = ['id', 'title', 'date', 'description', 'notes', 'location', 'created_at', 'updated_at', 'created_by', 'created_by_name', 'ai_summary']
        read_only_fields = ['created_by', 'created_at', 'updated_at', 'ai_summary']

class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    student_email = serializers.CharField(source='student.email', read_only=True)
    student_grade = serializers.IntegerField(source='student.grade', read_only=True)
    
    class Meta:
        model = Attendance
        fields = ['id', 'meeting', 'student', 'student_name', 'student_email', 'student_grade', 'is_present', 'recorded_by', 'recorded_at']
        read_only_fields = ['recorded_by', 'recorded_at']

class AttendanceListSerializer(serializers.Serializer):
    meeting = serializers.PrimaryKeyRelatedField(queryset=Meeting.objects.all())
    attendances = serializers.ListField(
        child=serializers.JSONField()
    )