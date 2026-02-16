import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Exam_management.settings')
django.setup()

from myapp.models import *
from django.contrib.auth.hashers import make_password
from datetime import date, time, timedelta

print("Adding sample data...")

# 1. Add Departments
dept1, _ = Department.objects.get_or_create(
    department_code='CSE',
    defaults={'department_name': 'Computer Science Engineering', 'hod': 'Dr. Rajesh Kumar'}
)
dept2, _ = Department.objects.get_or_create(
    department_code='ECE',
    defaults={'department_name': 'Electronics and Communication', 'hod': 'Dr. Priya Sharma'}
)
dept3, _ = Department.objects.get_or_create(
    department_code='MECH',
    defaults={'department_name': 'Mechanical Engineering', 'hod': 'Dr. Arun Patel'}
)
dept4, _ = Department.objects.get_or_create(
    department_code='CIVIL',
    defaults={'department_name': 'Civil Engineering', 'hod': 'Dr. Meena Reddy'}
)
print("✓ Departments added")

# 2. Add Staff
staff1, _ = Staff.objects.get_or_create(
    staff_id='STF001',
    defaults={
        'name': 'Prof. Suresh Kumar',
        'email': 'suresh@college.edu',
        'phone': '9876543210',
        'department': dept1,
        'designation': 'Professor',
        'qualification': 'Ph.D in Computer Science'
    }
)
staff2, _ = Staff.objects.get_or_create(
    staff_id='STF002',
    defaults={
        'name': 'Dr. Lakshmi Devi',
        'email': 'lakshmi@college.edu',
        'phone': '9876543211',
        'department': dept2,
        'designation': 'Associate Professor',
        'qualification': 'Ph.D in Electronics'
    }
)
staff3, _ = Staff.objects.get_or_create(
    staff_id='STF003',
    defaults={
        'name': 'Mr. Vijay Kumar',
        'email': 'vijay@college.edu',
        'phone': '9876543212',
        'department': dept3,
        'designation': 'Assistant Professor',
        'qualification': 'M.Tech in Mechanical'
    }
)
staff4, _ = Staff.objects.get_or_create(
    staff_id='STF004',
    defaults={
        'name': 'Mrs. Kavitha Rao',
        'email': 'kavitha@college.edu',
        'phone': '9876543213',
        'department': dept4,
        'designation': 'Assistant Professor',
        'qualification': 'M.Tech in Civil'
    }
)
print("✓ Staff added")

# 3. Add Students
student1, _ = Student.objects.get_or_create(
    student_id='STU001',
    defaults={
        'full_name': 'Rahul Sharma',
        'register_no': '2024CSE001',
        'department': dept1,
        'year': 2,
        'semester': 4,
        'email': 'rahul@student.edu',
        'phone': '9123456780',
        'address': '123 MG Road, Bangalore',
        'status': 'active'
    }
)
student2, _ = Student.objects.get_or_create(
    student_id='STU002',
    defaults={
        'full_name': 'Priya Reddy',
        'register_no': '2024ECE002',
        'department': dept2,
        'year': 3,
        'semester': 5,
        'email': 'priya@student.edu',
        'phone': '9123456781',
        'address': '456 Brigade Road, Bangalore',
        'status': 'active'
    }
)
student3, _ = Student.objects.get_or_create(
    student_id='STU003',
    defaults={
        'full_name': 'Arun Kumar',
        'register_no': '2024MECH003',
        'department': dept3,
        'year': 1,
        'semester': 2,
        'email': 'arun@student.edu',
        'phone': '9123456782',
        'address': '789 Indiranagar, Bangalore',
        'status': 'active'
    }
)
student4, _ = Student.objects.get_or_create(
    student_id='STU004',
    defaults={
        'full_name': 'Sneha Patel',
        'register_no': '2024CIVIL004',
        'department': dept4,
        'year': 4,
        'semester': 7,
        'email': 'sneha@student.edu',
        'phone': '9123456783',
        'address': '321 Koramangala, Bangalore',
        'status': 'active'
    }
)
print("✓ Students added")

# 4. Add Courses
course1, _ = Course.objects.get_or_create(
    course_code='CS101',
    defaults={
        'course_name': 'Data Structures',
        'department': dept1,
        'credits': 4,
        'semester': 3,
        'assigned_faculty': staff1
    }
)
course2, _ = Course.objects.get_or_create(
    course_code='EC201',
    defaults={
        'course_name': 'Digital Electronics',
        'department': dept2,
        'credits': 4,
        'semester': 4,
        'assigned_faculty': staff2
    }
)
course3, _ = Course.objects.get_or_create(
    course_code='ME301',
    defaults={
        'course_name': 'Thermodynamics',
        'department': dept3,
        'credits': 3,
        'semester': 5,
        'assigned_faculty': staff3
    }
)
course4, _ = Course.objects.get_or_create(
    course_code='CE401',
    defaults={
        'course_name': 'Structural Analysis',
        'department': dept4,
        'credits': 4,
        'semester': 6,
        'assigned_faculty': staff4
    }
)
print("✓ Courses added")

# 5. Add Exams
exam1, _ = Exam.objects.get_or_create(
    exam_name='Mid Semester Exam - April 2024',
    defaults={
        'exam_type': 'Internal',
        'start_date': date(2024, 4, 15),
        'end_date': date(2024, 4, 20),
        'duration': 120,
        'total_marks': 50,
        'semester': 4,
        'department': dept1
    }
)
exam2, _ = Exam.objects.get_or_create(
    exam_name='End Semester Exam - May 2024',
    defaults={
        'exam_type': 'Semester',
        'start_date': date(2024, 5, 10),
        'end_date': date(2024, 5, 25),
        'duration': 180,
        'total_marks': 100,
        'semester': 4,
        'department': dept1
    }
)
exam3, _ = Exam.objects.get_or_create(
    exam_name='Model Exam - March 2024',
    defaults={
        'exam_type': 'Model',
        'start_date': date(2024, 3, 5),
        'end_date': date(2024, 3, 10),
        'duration': 180,
        'total_marks': 100,
        'semester': 5,
        'department': dept2
    }
)
exam4, _ = Exam.objects.get_or_create(
    exam_name='Internal Assessment - February 2024',
    defaults={
        'exam_type': 'Internal',
        'start_date': date(2024, 2, 15),
        'end_date': date(2024, 2, 18),
        'duration': 90,
        'total_marks': 30,
        'semester': 2,
        'department': dept3
    }
)
print("✓ Exams added")

# 6. Add Exam Schedules
schedule1, _ = ExamSchedule.objects.get_or_create(
    exam=exam1,
    subject=course1,
    date=date(2024, 4, 15),
    defaults={
        'start_time': time(10, 0),
        'end_time': time(12, 0),
        'hall_number': 'Hall A-101',
        'invigilator': staff1
    }
)
schedule2, _ = ExamSchedule.objects.get_or_create(
    exam=exam2,
    subject=course2,
    date=date(2024, 5, 10),
    defaults={
        'start_time': time(14, 0),
        'end_time': time(17, 0),
        'hall_number': 'Hall B-202',
        'invigilator': staff2
    }
)
schedule3, _ = ExamSchedule.objects.get_or_create(
    exam=exam3,
    subject=course2,
    date=date(2024, 3, 5),
    defaults={
        'start_time': time(9, 0),
        'end_time': time(12, 0),
        'hall_number': 'Hall C-303',
        'invigilator': staff2
    }
)
schedule4, _ = ExamSchedule.objects.get_or_create(
    exam=exam4,
    subject=course3,
    date=date(2024, 2, 15),
    defaults={
        'start_time': time(10, 30),
        'end_time': time(12, 0),
        'hall_number': 'Hall D-404',
        'invigilator': staff3
    }
)
print("✓ Exam Schedules added")

# 7. Add Hall Tickets
ticket1, _ = HallTicket.objects.get_or_create(
    hall_ticket_number='HT2024001',
    defaults={
        'student': student1,
        'exam': exam1,
        'issued_date': date.today()
    }
)
ticket2, _ = HallTicket.objects.get_or_create(
    hall_ticket_number='HT2024002',
    defaults={
        'student': student2,
        'exam': exam2,
        'issued_date': date.today()
    }
)
ticket3, _ = HallTicket.objects.get_or_create(
    hall_ticket_number='HT2024003',
    defaults={
        'student': student3,
        'exam': exam4,
        'issued_date': date.today()
    }
)
ticket4, _ = HallTicket.objects.get_or_create(
    hall_ticket_number='HT2024004',
    defaults={
        'student': student4,
        'exam': exam3,
        'issued_date': date.today()
    }
)
print("✓ Hall Tickets added")

# 8. Add Marks
mark1, _ = MarksEntry.objects.get_or_create(
    student=student1,
    subject=course1,
    exam=exam1,
    defaults={
        'internal_marks': 42,
        'external_marks': 0,
        'remarks': 'Good performance'
    }
)
mark2, _ = MarksEntry.objects.get_or_create(
    student=student2,
    subject=course2,
    exam=exam2,
    defaults={
        'internal_marks': 18,
        'external_marks': 75,
        'remarks': 'Excellent'
    }
)
mark3, _ = MarksEntry.objects.get_or_create(
    student=student3,
    subject=course3,
    exam=exam4,
    defaults={
        'internal_marks': 25,
        'external_marks': 0,
        'remarks': 'Average'
    }
)
mark4, _ = MarksEntry.objects.get_or_create(
    student=student4,
    subject=course4,
    exam=exam3,
    defaults={
        'internal_marks': 20,
        'external_marks': 82,
        'remarks': 'Very Good'
    }
)
print("✓ Marks added")

# 9. Add Results
result1, _ = Result.objects.get_or_create(
    student=student1,
    exam=exam1,
    defaults={
        'total_marks': 420,
        'percentage': 84.0,
        'cgpa': 8.4,
        'result_status': 'Pass'
    }
)
result2, _ = Result.objects.get_or_create(
    student=student2,
    exam=exam2,
    defaults={
        'total_marks': 465,
        'percentage': 93.0,
        'cgpa': 9.3,
        'result_status': 'Pass'
    }
)
result3, _ = Result.objects.get_or_create(
    student=student3,
    exam=exam4,
    defaults={
        'total_marks': 125,
        'percentage': 62.5,
        'cgpa': 6.2,
        'result_status': 'Pass'
    }
)
result4, _ = Result.objects.get_or_create(
    student=student4,
    exam=exam3,
    defaults={
        'total_marks': 510,
        'percentage': 85.0,
        'cgpa': 8.5,
        'result_status': 'Pass'
    }
)
print("✓ Results added")

# 10. Add Notifications
notif1, _ = Notification.objects.get_or_create(
    title='Mid Semester Exam Schedule Released',
    defaults={
        'message': 'The mid semester examination schedule has been released. Please check your hall tickets.',
        'target_role': 'Student'
    }
)
notif2, _ = Notification.objects.get_or_create(
    title='Faculty Meeting on April 10',
    defaults={
        'message': 'All faculty members are requested to attend the meeting on April 10 at 3 PM in the conference hall.',
        'target_role': 'Staff'
    }
)
notif3, _ = Notification.objects.get_or_create(
    title='Library Closure Notice',
    defaults={
        'message': 'The library will remain closed on April 5 due to maintenance work.',
        'target_role': 'All'
    }
)
notif4, _ = Notification.objects.get_or_create(
    title='Result Declaration',
    defaults={
        'message': 'End semester examination results will be declared on May 30, 2024.',
        'target_role': 'Student'
    }
)
print("✓ Notifications added")

print("\n✅ All sample data added successfully!")
print("\nSummary:")
print("- 4 Departments")
print("- 4 Staff members")
print("- 4 Students")
print("- 4 Courses")
print("- 4 Exams")
print("- 4 Exam Schedules")
print("- 4 Hall Tickets")
print("- 4 Marks entries")
print("- 4 Results")
print("- 4 Notifications")
