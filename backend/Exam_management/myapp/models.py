from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator
import qrcode
from io import BytesIO
from django.core.files import File

# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'Admin')
        return self.create_user(email, username, password, **extra_fields)

# 1. Custom User Model
class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Staff', 'Staff'),
        ('Student', 'Student'),
    )
    
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Student')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.email

# Base Model for common fields
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        abstract = True

# 5. Department Model
class Department(BaseModel):
    department_name = models.CharField(max_length=200)
    department_code = models.CharField(max_length=20, unique=True)
    hod = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'departments'
        ordering = ['department_name']
    
    def __str__(self):
        return f"{self.department_code} - {self.department_name}"

# 3. Student Model
class Student(BaseModel):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile', null=True, blank=True)
    student_id = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=200)
    register_no = models.CharField(max_length=50, unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='students')
    year = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    semester = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)])
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    class Meta:
        db_table = 'students'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.register_no} - {self.full_name}"

# 4. Staff Model
class Staff(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile', null=True, blank=True)
    staff_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='staff_members')
    designation = models.CharField(max_length=100)
    qualification = models.CharField(max_length=200)
    
    class Meta:
        db_table = 'staff'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.staff_id} - {self.name}"

# 6. Course/Subject Model
class Course(BaseModel):
    course_code = models.CharField(max_length=20, unique=True)
    course_name = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='courses')
    credits = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    semester = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)])
    assigned_faculty = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='courses')
    
    class Meta:
        db_table = 'courses'
        ordering = ['course_code']
    
    def __str__(self):
        return f"{self.course_code} - {self.course_name}"

# 7. Exam Model
class Exam(BaseModel):
    EXAM_TYPE_CHOICES = (
        ('Internal', 'Internal'),
        ('Model', 'Model'),
        ('Semester', 'Semester'),
    )
    
    exam_name = models.CharField(max_length=200)
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPE_CHOICES)
    exam_date = models.DateField()
    duration = models.IntegerField(help_text='Duration in minutes')
    total_marks = models.IntegerField()
    semester = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)])
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='exams')
    
    class Meta:
        db_table = 'exams'
        ordering = ['-exam_date']
    
    def __str__(self):
        return f"{self.exam_name} - {self.exam_type}"

# 8. Exam Schedule Model
class ExamSchedule(BaseModel):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='schedules')
    subject = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exam_schedules')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    hall_number = models.CharField(max_length=50)
    invigilator = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, related_name='invigilation_duties')
    
    class Meta:
        db_table = 'exam_schedules'
        ordering = ['date', 'start_time']
        unique_together = ['exam', 'subject', 'date', 'start_time']
    
    def __str__(self):
        return f"{self.exam.exam_name} - {self.subject.course_name} - {self.date}"

# 9. Hall Ticket Model
class HallTicket(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='hall_tickets')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='hall_tickets')
    hall_ticket_number = models.CharField(max_length=50, unique=True)
    issued_date = models.DateField(auto_now_add=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    photo_url = models.ImageField(upload_to='student_photos/', blank=True, null=True)
    
    class Meta:
        db_table = 'hall_tickets'
        unique_together = ['student', 'exam']
    
    def save(self, *args, **kwargs):
        # Generate QR code
        if not self.qr_code:
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(f"HT-{self.hall_ticket_number}")
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            file_name = f'qr_{self.hall_ticket_number}.png'
            self.qr_code.save(file_name, File(buffer), save=False)
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.hall_ticket_number} - {self.student.full_name}"

# 10. Marks Entry Model
class MarksEntry(BaseModel):
    GRADE_CHOICES = (
        ('O', 'Outstanding'),
        ('A+', 'Excellent'),
        ('A', 'Very Good'),
        ('B+', 'Good'),
        ('B', 'Above Average'),
        ('C', 'Average'),
        ('F', 'Fail'),
    )
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
    subject = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='marks')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='marks')
    internal_marks = models.IntegerField(validators=[MinValueValidator(0)])
    external_marks = models.IntegerField(validators=[MinValueValidator(0)])
    total_marks = models.IntegerField(validators=[MinValueValidator(0)])
    grade = models.CharField(max_length=5, choices=GRADE_CHOICES, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'marks_entries'
        unique_together = ['student', 'subject', 'exam']
    
    def save(self, *args, **kwargs):
        # Auto calculate total marks
        self.total_marks = self.internal_marks + self.external_marks
        
        # Auto calculate grade
        percentage = (self.total_marks / self.exam.total_marks) * 100
        if percentage >= 90:
            self.grade = 'O'
        elif percentage >= 80:
            self.grade = 'A+'
        elif percentage >= 70:
            self.grade = 'A'
        elif percentage >= 60:
            self.grade = 'B+'
        elif percentage >= 50:
            self.grade = 'B'
        elif percentage >= 40:
            self.grade = 'C'
        else:
            self.grade = 'F'
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.student.full_name} - {self.subject.course_name} - {self.total_marks}"

# 11. Results Processing Model
class Result(BaseModel):
    RESULT_STATUS_CHOICES = (
        ('Pass', 'Pass'),
        ('Fail', 'Fail'),
    )
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results')
    total_marks = models.IntegerField()
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2)
    result_status = models.CharField(max_length=10, choices=RESULT_STATUS_CHOICES)
    
    class Meta:
        db_table = 'results'
        unique_together = ['student', 'exam']
    
    def __str__(self):
        return f"{self.student.full_name} - {self.exam.exam_name} - {self.result_status}"

# 12. Notifications Model
class Notification(BaseModel):
    TARGET_ROLE_CHOICES = (
        ('All', 'All'),
        ('Admin', 'Admin'),
        ('Staff', 'Staff'),
        ('Student', 'Student'),
    )
    
    title = models.CharField(max_length=200)
    message = models.TextField()
    target_role = models.CharField(max_length=20, choices=TARGET_ROLE_CHOICES, default='All')
    is_read = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title

# Audit Log Model
class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='audit_logs')
    action = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100)
    object_id = models.IntegerField(null=True, blank=True)
    changes = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'audit_logs'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user} - {self.action} - {self.model_name}"
