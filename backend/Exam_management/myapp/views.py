from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q, Count, Avg, Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from datetime import datetime, timedelta
from .models import (
    User, Student, Staff, Department, Course, Exam,
    ExamSchedule, HallTicket, MarksEntry, Result,
    Notification, AuditLog
)
from .serializers import (
    UserSerializer, RegisterSerializer, LoginSerializer, ProfileUpdateSerializer,
    StudentSerializer, StaffSerializer, DepartmentSerializer, CourseSerializer,
    ExamSerializer, ExamScheduleSerializer, HallTicketSerializer,
    MarksEntrySerializer, ResultSerializer, NotificationSerializer, AuditLogSerializer
)
from .permissions import IsAdmin, IsAdminOrStaff, IsAdminOrReadOnly

# Helper function to get client IP
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# Helper function to create audit log
def create_audit_log(user, action, model_name, object_id=None, changes=None, ip_address=None):
    AuditLog.objects.create(
        user=user,
        action=action,
        model_name=model_name,
        object_id=object_id,
        changes=changes,
        ip_address=ip_address
    )

# 1. Authentication Views
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        
        create_audit_log(user, 'REGISTER', 'User', user.id, None, get_client_ip(request))
        
        return Response({
            'message': 'User registered successfully',
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
    return Response({
        'message': 'Registration failed',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        
        # Only allow Admin role to login
        if user.role != 'Admin':
            return Response({
                'message': 'Access denied. Only Admin users can login.',
                'errors': {'role': ['Only Admin users are allowed to access this system.']}
            }, status=status.HTTP_403_FORBIDDEN)
        
        refresh = RefreshToken.for_user(user)
        
        create_audit_log(user, 'LOGIN', 'User', user.id, None, get_client_ip(request))
        
        return Response({
            'message': 'Login successful',
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_200_OK)
    return Response({
        'message': 'Login failed',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def profile_view(request):
    serializer = UserSerializer(request.user)
    return Response({
        'message': 'Profile retrieved successfully',
        'data': serializer.data
    }, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def profile_update_view(request):
    serializer = ProfileUpdateSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        
        create_audit_log(request.user, 'UPDATE_PROFILE', 'User', request.user.id, 
                        str(request.data), get_client_ip(request))
        
        return Response({
            'message': 'Profile updated successfully',
            'data': UserSerializer(request.user).data
        }, status=status.HTTP_200_OK)
    return Response({
        'message': 'Profile update failed',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

# 2. Dashboard Analytics View
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_view(request):
    # Get counts
    total_students = Student.objects.filter(is_deleted=False).count()
    total_staff = Staff.objects.filter(is_deleted=False).count()
    total_departments = Department.objects.filter(is_deleted=False).count()
    total_courses = Course.objects.filter(is_deleted=False).count()
    
    # Upcoming exams (next 30 days)
    today = datetime.now().date()
    upcoming_exams = Exam.objects.filter(
        exam_date__gte=today,
        exam_date__lte=today + timedelta(days=30),
        is_deleted=False
    ).count()
    
    # Attendance overview (placeholder)
    attendance_overview = {
        'present': 0,
        'absent': 0,
        'percentage': 0
    }
    
    # Result summary
    total_results = Result.objects.filter(is_deleted=False).count()
    passed_results = Result.objects.filter(result_status='Pass', is_deleted=False).count()
    failed_results = Result.objects.filter(result_status='Fail', is_deleted=False).count()
    
    result_summary = {
        'total': total_results,
        'passed': passed_results,
        'failed': failed_results,
        'pass_percentage': round((passed_results / total_results * 100), 2) if total_results > 0 else 0
    }
    
    return Response({
        'message': 'Dashboard data retrieved successfully',
        'data': {
            'total_students': total_students,
            'total_staff': total_staff,
            'total_departments': total_departments,
            'total_courses': total_courses,
            'upcoming_exams': upcoming_exams,
            'attendance_overview': attendance_overview,
            'result_summary': result_summary
        }
    }, status=status.HTTP_200_OK)

# 3. Student ViewSet
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.filter(is_deleted=False)
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['department', 'semester', 'year', 'status']
    search_fields = ['full_name', 'register_no', 'email', 'student_id']
    ordering_fields = ['created_at', 'full_name', 'register_no']
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            student = serializer.save()
            create_audit_log(request.user, 'CREATE', 'Student', student.id, 
                           str(request.data), get_client_ip(request))
            return Response({
                'message': 'Student created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': 'Student creation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            create_audit_log(request.user, 'UPDATE', 'Student', instance.id, 
                           str(request.data), get_client_ip(request))
            return Response({
                'message': 'Student updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            'message': 'Student update failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        create_audit_log(request.user, 'DELETE', 'Student', instance.id, 
                       None, get_client_ip(request))
        return Response({
            'message': 'Student deleted successfully'
        }, status=status.HTTP_200_OK)

# 4. Staff ViewSet
class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.filter(is_deleted=False)
    serializer_class = StaffSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['department', 'designation']
    search_fields = ['name', 'email', 'staff_id']
    ordering_fields = ['created_at', 'name']
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            staff = serializer.save()
            create_audit_log(request.user, 'CREATE', 'Staff', staff.id, 
                           str(request.data), get_client_ip(request))
            return Response({
                'message': 'Staff created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': 'Staff creation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            create_audit_log(request.user, 'UPDATE', 'Staff', instance.id, 
                           str(request.data), get_client_ip(request))
            return Response({
                'message': 'Staff updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            'message': 'Staff update failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        create_audit_log(request.user, 'DELETE', 'Staff', instance.id, 
                       None, get_client_ip(request))
        return Response({
            'message': 'Staff deleted successfully'
        }, status=status.HTTP_200_OK)

# 5. Department ViewSet
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.filter(is_deleted=False)
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['department_name', 'department_code']
    ordering_fields = ['created_at', 'department_name']
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            dept = serializer.save()
            create_audit_log(request.user, 'CREATE', 'Department', dept.id, 
                           str(request.data), get_client_ip(request))
            return Response({
                'message': 'Department created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': 'Department creation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            create_audit_log(request.user, 'UPDATE', 'Department', instance.id, 
                           str(request.data), get_client_ip(request))
            return Response({
                'message': 'Department updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            'message': 'Department update failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        create_audit_log(request.user, 'DELETE', 'Department', instance.id, 
                       None, get_client_ip(request))
        return Response({
            'message': 'Department deleted successfully'
        }, status=status.HTTP_200_OK)

# 6. Course ViewSet
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.filter(is_deleted=False)
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['department', 'semester', 'assigned_faculty']
    search_fields = ['course_name', 'course_code']
    ordering_fields = ['created_at', 'course_name']
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            course = serializer.save()
            create_audit_log(request.user, 'CREATE', 'Course', course.id, 
                           str(request.data), get_client_ip(request))
            return Response({
                'message': 'Course created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': 'Course creation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            create_audit_log(request.user, 'UPDATE', 'Course', instance.id, 
                           str(request.data), get_client_ip(request))
            return Response({
                'message': 'Course updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            'message': 'Course update failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        create_audit_log(request.user, 'DELETE', 'Course', instance.id, 
                       None, get_client_ip(request))
        return Response({
            'message': 'Course deleted successfully'
        }, status=status.HTTP_200_OK)

# 7. Exam ViewSet
class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.filter(is_deleted=False)
    serializer_class = ExamSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['exam_type', 'semester', 'department']
    search_fields = ['exam_name']
    ordering_fields = ['start_date', 'created_at']
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            exam = serializer.save()
            create_audit_log(request.user, 'CREATE', 'Exam', exam.id, 
                           str(request.data), get_client_ip(request))
            return Response({
                'message': 'Exam created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': 'Exam creation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            create_audit_log(request.user, 'UPDATE', 'Exam', instance.id, 
                           str(request.data), get_client_ip(request))
            return Response({
                'message': 'Exam updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            'message': 'Exam update failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        create_audit_log(request.user, 'DELETE', 'Exam', instance.id, 
                       None, get_client_ip(request))
        return Response({
            'message': 'Exam deleted successfully'
        }, status=status.HTTP_200_OK)

# 8. Exam Schedule ViewSet
class ExamScheduleViewSet(viewsets.ModelViewSet):
    queryset = ExamSchedule.objects.filter(is_deleted=False)
    serializer_class = ExamScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['exam', 'subject', 'date']
    search_fields = ['hall_number']
    ordering_fields = ['date', 'start_time']
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            schedule = serializer.save()
            create_audit_log(request.user, 'CREATE', 'ExamSchedule', schedule.id, 
                           str(request.data), get_client_ip(request))
            return Response({
                'message': 'Exam schedule created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': 'Exam schedule creation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            create_audit_log(request.user, 'UPDATE', 'ExamSchedule', instance.id, 
                           str(request.data), get_client_ip(request))
            return Response({
                'message': 'Exam schedule updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            'message': 'Exam schedule update failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        create_audit_log(request.user, 'DELETE', 'ExamSchedule', instance.id, 
                       None, get_client_ip(request))
        return Response({
            'message': 'Exam schedule deleted successfully'
        }, status=status.HTTP_200_OK)

# 9. Hall Ticket ViewSet
class HallTicketViewSet(viewsets.ModelViewSet):
    queryset = HallTicket.objects.filter(is_deleted=False)
    serializer_class = HallTicketSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['student', 'exam', 'hall_ticket_number']
    search_fields = ['hall_ticket_number']
    
    @action(detail=False, methods=['get'], url_path='student/(?P<student_id>[^/.]+)')
    def get_by_student(self, request, student_id=None):
        hall_tickets = self.queryset.filter(student_id=student_id)
        serializer = self.get_serializer(hall_tickets, many=True)
        return Response({
            'message': 'Hall tickets retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            hall_ticket = serializer.save()
            create_audit_log(request.user, 'CREATE', 'HallTicket', hall_ticket.id, 
                           str(request.data), get_client_ip(request))
            return Response({
                'message': 'Hall ticket created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': 'Hall ticket creation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

# 10. Marks Entry ViewSet
class MarksEntryViewSet(viewsets.ModelViewSet):
    queryset = MarksEntry.objects.filter(is_deleted=False)
    serializer_class = MarksEntrySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['student', 'subject', 'exam', 'grade']
    search_fields = ['student__full_name', 'subject__course_name']
    ordering_fields = ['total_marks', 'created_at']
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            marks = serializer.save()
            create_audit_log(request.user, 'CREATE', 'MarksEntry', marks.id, 
                           str(request.data), get_client_ip(request))
            return Response({
                'message': 'Marks entry created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': 'Marks entry creation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            create_audit_log(request.user, 'UPDATE', 'MarksEntry', instance.id, 
                           str(request.data), get_client_ip(request))
            return Response({
                'message': 'Marks entry updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            'message': 'Marks entry update failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        create_audit_log(request.user, 'DELETE', 'MarksEntry', instance.id, 
                       None, get_client_ip(request))
        return Response({
            'message': 'Marks entry deleted successfully'
        }, status=status.HTTP_200_OK)

# 11. Result ViewSet
class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.filter(is_deleted=False)
    serializer_class = ResultSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['student', 'exam', 'result_status']
    search_fields = ['student__full_name', 'student__register_no']
    ordering_fields = ['percentage', 'cgpa', 'created_at']
    
    @action(detail=False, methods=['get'], url_path='student/(?P<student_id>[^/.]+)')
    def get_by_student(self, request, student_id=None):
        results = self.queryset.filter(student_id=student_id)
        serializer = self.get_serializer(results, many=True)
        return Response({
            'message': 'Results retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            create_audit_log(request.user, 'CREATE', 'Result', result.id, 
                           str(request.data), get_client_ip(request))
            return Response({
                'message': 'Result created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': 'Result creation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            create_audit_log(request.user, 'UPDATE', 'Result', instance.id, 
                           str(request.data), get_client_ip(request))
            return Response({
                'message': 'Result updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            'message': 'Result update failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

# 12. Notification ViewSet
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.filter(is_deleted=False)
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['target_role', 'is_read']
    search_fields = ['title', 'message']
    ordering_fields = ['created_at']
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'Admin':
            return self.queryset
        else:
            return self.queryset.filter(Q(target_role='All') | Q(target_role=user.role))
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            notification = serializer.save()
            create_audit_log(request.user, 'CREATE', 'Notification', notification.id, 
                           str(request.data), get_client_ip(request))
            return Response({
                'message': 'Notification created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': 'Notification creation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            create_audit_log(request.user, 'UPDATE', 'Notification', instance.id, 
                           str(request.data), get_client_ip(request))
            return Response({
                'message': 'Notification updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            'message': 'Notification update failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        create_audit_log(request.user, 'DELETE', 'Notification', instance.id, 
                       None, get_client_ip(request))
        return Response({
            'message': 'Notification deleted successfully'
        }, status=status.HTTP_200_OK)
