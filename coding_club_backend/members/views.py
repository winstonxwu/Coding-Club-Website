from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Member, Meeting, Attendance
from .serializers import MemberSerializer, MeetingSerializer, AttendanceSerializer, AttendanceListSerializer
from .utils import generate_meeting_summary

User = get_user_model()

class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.account_type == 'teacher'

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsTeacher()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        return Member.objects.all()

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        user = authenticate(request, email=email, password=password)
        
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'token': str(refresh.access_token),
                'refresh': str(refresh),
                'user': MemberSerializer(user).data
            })
        return Response(
            {'message': 'Invalid credentials'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')
        account_type = request.data.get('account_type')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        grade = request.data.get('grade')

        if not all([email, password, account_type]):
            return Response(
                {'detail': 'Email, password, and account type are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if account_type not in ['teacher', 'student']:
            return Response(
                {'detail': 'Invalid account type'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if Member.objects.filter(email=email).exists():
            return Response(
                {'detail': 'User with this email already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )

        member = Member.objects.create_user(
            email=email,
            password=password,
            account_type=account_type,
            first_name=first_name,
            last_name=last_name,
            grade=grade
        )
        
        refresh = RefreshToken.for_user(member)
        
        return Response({
            'detail': 'User registered successfully',
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'detail': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsTeacher()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        meeting = serializer.save(created_by=self.request.user)
        
        title = meeting.title
        description = meeting.description or ""
        notes = meeting.notes or ""
        
        ai_summary = generate_meeting_summary(title, description, notes)
        meeting.ai_summary = ai_summary
        meeting.save()

    def perform_update(self, serializer):
        meeting = serializer.save()
        
        title = meeting.title
        description = meeting.description or ""
        notes = meeting.notes or ""
        
        ai_summary = generate_meeting_summary(title, description, notes)
        meeting.ai_summary = ai_summary
        meeting.save()

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def perform_create(self, serializer):
        serializer.save(recorded_by=self.request.user)

    @action(detail=False, methods=['post'])
    def record_batch(self, request):
        serializer = AttendanceListSerializer(data=request.data)
        if serializer.is_valid():
            meeting = serializer.validated_data['meeting']
            attendances = serializer.validated_data['attendances']
            
            # Clear existing attendance for this meeting
            Attendance.objects.filter(meeting=meeting).delete()
            
            # Create new attendance records
            created_records = []
            for attendance_data in attendances:
                student_id = attendance_data.get('student_id')
                is_present = attendance_data.get('is_present', False)
                
                try:
                    student = Member.objects.get(id=student_id, account_type='student')
                    attendance = Attendance.objects.create(
                        meeting=meeting,
                        student=student,
                        is_present=is_present,
                        recorded_by=request.user
                    )
                    created_records.append(attendance)
                except Member.DoesNotExist:
                    continue
            
            return Response({
                'message': f'Successfully recorded attendance for {len(created_records)} students',
                'meeting_id': meeting.id
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def meeting_attendance(self, request):
        meeting_id = request.query_params.get('meeting_id')
        if not meeting_id:
            return Response({'detail': 'meeting_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            meeting = Meeting.objects.get(id=meeting_id)
            attendances = Attendance.objects.filter(meeting=meeting)
            serializer = self.get_serializer(attendances, many=True)
            return Response(serializer.data)
        except Meeting.DoesNotExist:
            return Response({'detail': 'Meeting not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def current_user(request):
    serializer = MemberSerializer(request.user)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, IsTeacher])
def students_list(request):
    students = Member.objects.filter(account_type='student')
    serializer = MemberSerializer(students, many=True)
    return Response(serializer.data)