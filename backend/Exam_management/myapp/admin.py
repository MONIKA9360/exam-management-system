from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, Student, Staff, Department, Course, Exam,
    ExamSchedule, HallTicket, MarksEntry, Result,
    Notification, AuditLog
)

# Custom User Admin
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'username', 'role', 'is_active', 'is_staff', 'date_joined']
    list_filter = ['role', 'is_active', 'is_staff']
    search_fields = ['email', 'username']
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('username', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'role', 'is_staff', 'is_active')}
        ),
    )

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'full_name', 'register_no', 'department', 'semester', 'status', 'created_at']
    list_filter = ['department', 'semester', 'year', 'status', 'is_deleted']
    search_fields = ['full_name', 'register_no', 'email', 'student_id']
    ordering = ['-created_at']

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['staff_id', 'name', 'email', 'department', 'designation', 'created_at']
    list_filter = ['department', 'designation', 'is_deleted']
    search_fields = ['name', 'email', 'staff_id']
    ordering = ['name']

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['department_code', 'department_name', 'hod', 'created_at']
    list_filter = ['is_deleted']
    search_fields = ['department_name', 'department_code']
    ordering = ['department_name']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_code', 'course_name', 'department', 'semester', 'credits', 'assigned_faculty']
    list_filter = ['department', 'semester', 'is_deleted']
    search_fields = ['course_name', 'course_code']
    ordering = ['course_code']

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['exam_name', 'exam_type', 'start_date', 'end_date', 'semester', 'department']
    list_filter = ['exam_type', 'semester', 'department', 'is_deleted']
    search_fields = ['exam_name']
    ordering = ['-start_date']

@admin.register(ExamSchedule)
class ExamScheduleAdmin(admin.ModelAdmin):
    list_display = ['exam', 'subject', 'date', 'start_time', 'end_time', 'hall_number', 'invigilator']
    list_filter = ['exam', 'date', 'is_deleted']
    search_fields = ['hall_number']
    ordering = ['date', 'start_time']

@admin.register(HallTicket)
class HallTicketAdmin(admin.ModelAdmin):
    list_display = ['hall_ticket_number', 'student', 'exam', 'issued_date']
    list_filter = ['exam', 'issued_date', 'is_deleted']
    search_fields = ['hall_ticket_number', 'student__full_name']
    ordering = ['-issued_date']

@admin.register(MarksEntry)
class MarksEntryAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'exam', 'internal_marks', 'external_marks', 'total_marks', 'grade']
    list_filter = ['exam', 'grade', 'is_deleted']
    search_fields = ['student__full_name', 'subject__course_name']
    ordering = ['-created_at']

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam', 'total_marks', 'percentage', 'cgpa', 'result_status']
    list_filter = ['exam', 'result_status', 'is_deleted']
    search_fields = ['student__full_name', 'student__register_no']
    ordering = ['-created_at']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'target_role', 'is_read', 'created_at']
    list_filter = ['target_role', 'is_read', 'is_deleted']
    search_fields = ['title', 'message']
    ordering = ['-created_at']

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'model_name', 'object_id', 'timestamp']
    list_filter = ['action', 'model_name', 'timestamp']
    search_fields = ['user__email', 'action', 'model_name']
    ordering = ['-timestamp']
    readonly_fields = ['user', 'action', 'model_name', 'object_id', 'changes', 'ip_address', 'timestamp']
