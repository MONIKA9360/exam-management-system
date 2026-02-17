import os
import django
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Exam_management.settings')
django.setup()

from myapp.models import (
    Department, Staff, Student, Course, Exam,
    ExamSchedule, HallTicket, MarksEntry, Result, Notification
)

print("Adding sample data to Supabase...")

# 1. Departments
print("\n1. Creating Departments...")
dept1 = Department.objects.create(
    department_code="DEPT001",
    department_name="Computer Science and Engineering",
    hod="Dr. Rajesh Kumar"
)
dept2 = Department.objects.create(
    department_code="DEPT002",
    department_name="Electronics and Communication",
    hod="Dr. Priya Sharma"
)
dept3 = Department.objects.create(
    department_code="DEPT003",
    department_name="Mechanical Engineering",
    hod="Dr. Vijay Kumar"
)
dept4 = Department.objects.create(
    department_code="DEPT004",
    department_name="Civil Engineering",
    hod="Dr. Kavitha Rao"
)
print(f"✓ Created {Department.objects.count()} departments")

# 2. Staff
print("\n2. Creating Staff...")
staff1 = Staff.objects.create(
    staff_id="STF001",
    name="Prof. Suresh Kumar",
    email="suresh@college.edu",
    phone="9876543210",
    department=dept1,
    designation="Associate Professor",
    qualification="Ph.D in Computer Science"
)
staff2 = Staff.objects.create(
    staff_id="STF002",
    name="Dr. Lakshmi Devi",
    email="lakshmi@college.edu",
    phone="9876543211",
    department=dept2,
    designation="Assistant Professor",
    qualification="Ph.D in Electronics"
)
staff3 = Staff.objects.create(
    staff_id="STF003",
    name="Mr. Vijay Kumar",
    email="vijay@college.edu",
    phone="9876543212",
    department=dept3,
    designation="Assistant Professor",
    qualification="M.Tech in Mechanical"
)
staff4 = Staff.objects.create(
    staff_id="STF004",
    name="Mrs. Kavitha Rao",
    email="kavitha@college.edu",
    phone="9876543213",
    department=dept4,
    designation="Assistant Professor",
    qualification="M.Tech in Civil"
)
print(f"✓ Created {Staff.objects.count()} staff members")

# 3. Students
print("\n3. Creating Students...")
student1 = Student.objects.create(
    student_id="STU001",
    full_name="Sneha Patel",
    register_no="2024CIVIL004",
    department=dept4,
    year=1,
    semester=7,
    email="sneha@student.edu",
    phone="9876543220",
    address="123 Main St, Chennai",
    status="active"
)
student2 = Student.objects.create(
    student_id="STU002",
    full_name="Arun Kumar",
    register_no="2024MECH003",
    department=dept3,
    year=2,
    semester=2,
    email="arun@student.edu",
    phone="9876543221",
    address="456 Park Ave, Chennai",
    status="active"
)
student3 = Student.objects.create(
    student_id="STU003",
    full_name="Priya Reddy",
    register_no="2024ECE002",
    department=dept2,
    year=3,
    semester=5,
    email="priya@student.edu",
    phone="9876543222",
    address="789 Lake Rd, Chennai",
    status="active"
)
student4 = Student.objects.create(
    student_id="STU004",
    full_name="MONIKA M",
    register_no="731501",
    department=dept1,
    year=4,
    semester=8,
    email="monika@student.edu",
    phone="9876543223",
    address="321 Hill St, Chennai",
    status="active"
)
print(f"✓ Created {Student.objects.count()} students")

# 4. Courses
print("\n4. Creating Courses...")
course1 = Course.objects.create(
    course_code="CRS001",
    course_name="Data Structures and Algorithms",
    department=dept1,
    credits=4,
    semester=3,
    assigned_faculty=staff1
)
course2 = Course.objects.create(
    course_code="CRS002",
    course_name="Digital Signal Processing",
    department=dept2,
    credits=4,
    semester=5,
    assigned_faculty=staff2
)
course3 = Course.objects.create(
    course_code="CRS003",
    course_name="Thermodynamics",
    department=dept3,
    credits=3,
    semester=4,
    assigned_faculty=staff3
)
course4 = Course.objects.create(
    course_code="CRS004",
    course_name="Structural Analysis",
    department=dept4,
    credits=4,
    semester=6,
    assigned_faculty=staff4
)
print(f"✓ Created {Course.objects.count()} courses")

# 5. Exams
print("\n5. Creating Exams...")
today = date.today()
exam1 = Exam.objects.create(
    exam_name="Mid Semester Exam",
    exam_type="Internal",
    exam_date=today + timedelta(days=10),
    duration=120,
    total_marks=50,
    semester=4,
    department=dept1
)
exam2 = Exam.objects.create(
    exam_name="End Semester Exam - May 2025",
    exam_type="Semester",
    exam_date=today + timedelta(days=30),
    duration=180,
    total_marks=100,
    semester=4,
    department=dept2
)
exam3 = Exam.objects.create(
    exam_name="Model Exam - March 2025",
    exam_type="Model",
    exam_date=today + timedelta(days=20),
    duration=180,
    total_marks=100,
    semester=5,
    department=dept3
)
print(f"✓ Created {Exam.objects.count()} exams")

# 6. Exam Schedules
print("\n6. Creating Exam Schedules...")
ExamSchedule.objects.create(
    exam=exam1,
    subject=course1,
    date=today + timedelta(days=10),
    start_time="09:00:00",
    end_time="11:00:00",
    hall_number="Hall A-101",
    invigilator=staff1
)
ExamSchedule.objects.create(
    exam=exam2,
    subject=course2,
    date=today + timedelta(days=30),
    start_time="14:00:00",
    end_time="17:00:00",
    hall_number="Hall B-202",
    invigilator=staff2
)
print(f"✓ Created {ExamSchedule.objects.count()} exam schedules")

# 7. Hall Tickets
print("\n7. Creating Hall Tickets...")
HallTicket.objects.create(
    student=student1,
    exam=exam1,
    hall_ticket_number="HT2024001"
)
HallTicket.objects.create(
    student=student2,
    exam=exam2,
    hall_ticket_number="HT2024002"
)
HallTicket.objects.create(
    student=student3,
    exam=exam3,
    hall_ticket_number="HT2024003"
)
HallTicket.objects.create(
    student=student4,
    exam=exam1,
    hall_ticket_number="HT2024004"
)
print(f"✓ Created {HallTicket.objects.count()} hall tickets")

# 8. Marks
print("\n8. Creating Marks Entries...")
MarksEntry.objects.create(
    student=student1,
    subject=course1,
    exam=exam1,
    internal_marks=18,
    external_marks=72,
    total_marks=90,
    grade="A+"
)
MarksEntry.objects.create(
    student=student2,
    subject=course2,
    exam=exam2,
    internal_marks=16,
    external_marks=68,
    total_marks=84,
    grade="A"
)
print(f"✓ Created {MarksEntry.objects.count()} marks entries")

# 9. Results
print("\n9. Creating Results...")
Result.objects.create(
    student=student1,
    exam=exam1,
    total_marks=450,
    percentage=90.0,
    cgpa=9.0,
    result_status="Pass"
)
Result.objects.create(
    student=student2,
    exam=exam2,
    total_marks=420,
    percentage=84.0,
    cgpa=8.4,
    result_status="Pass"
)
print(f"✓ Created {Result.objects.count()} results")

# 10. Notifications
print("\n10. Creating Notifications...")
Notification.objects.create(
    title="Mid Semester Exam Schedule Released",
    message="The mid semester exam schedule has been released. Check your hall tickets.",
    target_role="Student"
)
Notification.objects.create(
    title="Faculty Meeting on March 15",
    message="All faculty members are requested to attend the meeting.",
    target_role="Staff"
)
print(f"✓ Created {Notification.objects.count()} notifications")

print("\n" + "="*60)
print("SAMPLE DATA ADDED SUCCESSFULLY!")
print("="*60)
print(f"Departments:    {Department.objects.count()}")
print(f"Staff:          {Staff.objects.count()}")
print(f"Students:       {Student.objects.count()}")
print(f"Courses:        {Course.objects.count()}")
print(f"Exams:          {Exam.objects.count()}")
print(f"Exam Schedules: {ExamSchedule.objects.count()}")
print(f"Hall Tickets:   {HallTicket.objects.count()}")
print(f"Marks Entries:  {MarksEntry.objects.count()}")
print(f"Results:        {Result.objects.count()}")
print(f"Notifications:  {Notification.objects.count()}")
print("="*60)
print("\nNow refresh your dashboard to see the data!")
