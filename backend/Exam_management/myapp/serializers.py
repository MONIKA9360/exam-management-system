from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import (
    User, Student, Staff, Department, Course, Exam, 
    ExamSchedule, HallTicket, MarksEntry, Result, 
    Notification, AuditLog
)

# 1. User & Authentication Serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'is_active', 'date_joined']
        read_only_fields = ['id', 'date_joined']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role', 'Student')
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            data['user'] = user
        else:
            raise serializers.ValidationError('Must include email and password')
        
        return data

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

# 5. Department Serializer
class DepartmentSerializer(serializers.ModelSerializer):
    total_students = serializers.SerializerMethodField()
    total_staff = serializers.SerializerMethodField()
    
    class Meta:
        model = Department
        fields = ['id', 'department_name', 'department_code', 'hod', 'description', 
                  'total_students', 'total_staff', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_total_students(self, obj):
        return obj.students.filter(is_deleted=False).count()
    
    def get_total_staff(self, obj):
        return obj.staff_members.filter(is_deleted=False).count()
    
    def validate_department_code(self, value):
        if Department.objects.filter(department_code=value, is_deleted=False).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError('Department Code already exists')
        return value
    
    def validate_department_name(self, value):
        if Department.objects.filter(department_name=value, is_deleted=False).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError('Department Name already exists')
        return value

# 4. Staff Serializer
class StaffSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.department_name', read_only=True)
    
    class Meta:
        model = Staff
        fields = ['id', 'staff_id', 'name', 'email', 'phone', 'department', 
                  'department_name', 'designation', 'qualification', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_staff_id(self, value):
        if Staff.objects.filter(staff_id=value, is_deleted=False).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError('Staff ID already exists')
        return value
    
    def validate_email(self, value):
        if Staff.objects.filter(email=value, is_deleted=False).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError('Email already exists')
        return value
    
    def validate_phone(self, value):
        if Staff.objects.filter(phone=value, is_deleted=False).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError('Phone number already exists')
        return value

# 3. Student Serializer
class StudentSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.department_name', read_only=True)
    
    class Meta:
        model = Student
        fields = ['id', 'student_id', 'full_name', 'register_no', 'department', 
                  'department_name', 'year', 'semester', 'email', 'phone', 
                  'address', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_student_id(self, value):
        if Student.objects.filter(student_id=value, is_deleted=False).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError('Student ID already exists')
        return value
    
    def validate_register_no(self, value):
        if Student.objects.filter(register_no=value, is_deleted=False).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError('Register Number already exists')
        return value
    
    def validate_email(self, value):
        if Student.objects.filter(email=value, is_deleted=False).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError('Email already exists')
        return value
    
    def validate_phone(self, value):
        if Student.objects.filter(phone=value, is_deleted=False).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError('Phone number already exists')
        return value
        if Student.objects.filter(email=value, is_deleted=False).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError('Student with this email already exists')
        return value
    
    def validate_register_no(self, value):
        if Student.objects.filter(register_no=value, is_deleted=False).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError('Student with this register number already exists')
        return value

# 6. Course Serializer
class CourseSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.department_name', read_only=True)
    faculty_name = serializers.CharField(source='assigned_faculty.name', read_only=True)
    
    class Meta:
        model = Course
        fields = ['id', 'course_code', 'course_name', 'department', 'department_name',
                  'credits', 'semester', 'assigned_faculty', 'faculty_name', 
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_course_code(self, value):
        if Course.objects.filter(course_code=value, is_deleted=False).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError('Course Code already exists')
        return value

# 7. Exam Serializer
class ExamSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.department_name', read_only=True)
    
    class Meta:
        model = Exam
        fields = ['id', 'exam_name', 'exam_type', 'exam_date', 
                  'duration', 'total_marks', 'semester', 'department', 
                  'department_name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

# 8. Exam Schedule Serializer
class ExamScheduleSerializer(serializers.ModelSerializer):
    exam_name = serializers.CharField(source='exam.exam_name', read_only=True)
    subject_name = serializers.CharField(source='subject.course_name', read_only=True)
    invigilator_name = serializers.CharField(source='invigilator.name', read_only=True)
    
    class Meta:
        model = ExamSchedule
        fields = ['id', 'exam', 'exam_name', 'subject', 'subject_name', 
                  'date', 'start_time', 'end_time', 'hall_number', 
                  'invigilator', 'invigilator_name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate(self, data):
        # Check time clash
        if data.get('end_time') and data.get('start_time'):
            if data['end_time'] <= data['start_time']:
                raise serializers.ValidationError('End time must be after start time')
        
        # Check for hall clash
        if data.get('hall_number') and data.get('date') and data.get('start_time'):
            clash = ExamSchedule.objects.filter(
                hall_number=data['hall_number'],
                date=data['date'],
                start_time__lt=data.get('end_time', data['start_time']),
                end_time__gt=data['start_time'],
                is_deleted=False
            ).exclude(id=self.instance.id if self.instance else None)
            
            if clash.exists():
                raise serializers.ValidationError('Hall is already booked for this time slot')
        
        return data

# 9. Hall Ticket Serializer
class HallTicketSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    register_no = serializers.CharField(source='student.register_no', read_only=True)
    exam_name = serializers.CharField(source='exam.exam_name', read_only=True)
    department_name = serializers.CharField(source='student.department.department_name', read_only=True)
    
    class Meta:
        model = HallTicket
        fields = ['id', 'student', 'student_name', 'register_no', 
                  'exam', 'exam_name', 'hall_ticket_number', 'issued_date', 
                  'qr_code', 'photo_url', 'department_name', 'created_at']
        read_only_fields = ['id', 'issued_date', 'qr_code', 'created_at']

# 10. Marks Entry Serializer
class MarksEntrySerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    subject_name = serializers.CharField(source='subject.course_name', read_only=True)
    exam_name = serializers.CharField(source='exam.exam_name', read_only=True)
    
    class Meta:
        model = MarksEntry
        fields = ['id', 'student', 'student_name', 'subject', 'subject_name', 
                  'exam', 'exam_name', 'internal_marks', 'external_marks', 
                  'total_marks', 'grade', 'remarks', 'created_at', 'updated_at']
        read_only_fields = ['id', 'total_marks', 'grade', 'created_at', 'updated_at']
    
    def validate(self, data):
        exam = data.get('exam')
        internal_marks = data.get('internal_marks', 0)
        external_marks = data.get('external_marks', 0)
        
        if exam:
            total = internal_marks + external_marks
            if total > exam.total_marks:
                raise serializers.ValidationError(
                    f'Total marks ({total}) cannot exceed exam total marks ({exam.total_marks})'
                )
        
        return data

# 11. Result Serializer
class ResultSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    student_register_no = serializers.CharField(source='student.register_no', read_only=True)
    exam_name = serializers.CharField(source='exam.exam_name', read_only=True)
    
    class Meta:
        model = Result
        fields = ['id', 'student', 'student_name', 'student_register_no', 
                  'exam', 'exam_name', 'total_marks', 'percentage', 'cgpa', 
                  'result_status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

# 12. Notification Serializer
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'target_role', 'is_read', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

# Audit Log Serializer
class AuditLogSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = AuditLog
        fields = ['id', 'user', 'user_email', 'action', 'model_name', 
                  'object_id', 'changes', 'ip_address', 'timestamp']
        read_only_fields = ['id', 'timestamp']
