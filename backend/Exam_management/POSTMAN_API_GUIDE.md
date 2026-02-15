# EXAM MANAGEMENT SYSTEM - POSTMAN API TESTING GUIDE

## Base URL
```
http://localhost:8000/api/
```

## Authentication
All APIs (except register and login) require JWT token in headers:
```
Authorization: Bearer <your_access_token>
```

---

## 1️⃣ AUTHENTICATION & ROLE MANAGEMENT

### 1.1 Register User
**POST** `/api/auth/register/`

**Request Body:**
```json
{
    "username": "admin_user",
    "email": "admin@example.com",
    "password": "Admin@123",
    "role": "Admin"
}
```

**Response:**
```json
{
    "message": "User registered successfully",
    "user": {
        "id": 1,
        "username": "admin_user",
        "email": "admin@example.com",
        "role": "Admin",
        "is_active": true,
        "date_joined": "2024-02-13T10:30:00Z"
    },
    "tokens": {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
    }
}
```

### 1.2 Login
**POST** `/api/auth/login/`

**Request Body:**
```json
{
    "email": "admin@example.com",
    "password": "Admin@123"
}
```

**Response:**
```json
{
    "message": "Login successful",
    "user": {
        "id": 1,
        "username": "admin_user",
        "email": "admin@example.com",
        "role": "Admin",
        "is_active": true,
        "date_joined": "2024-02-13T10:30:00Z"
    },
    "tokens": {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
    }
}
```

### 1.3 Get Profile
**GET** `/api/auth/profile/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
    "message": "Profile retrieved successfully",
    "data": {
        "id": 1,
        "username": "admin_user",
        "email": "admin@example.com",
        "role": "Admin",
        "is_active": true,
        "date_joined": "2024-02-13T10:30:00Z"
    }
}
```

### 1.4 Update Profile
**PUT** `/api/auth/profile/update/`

**Request Body:**
```json
{
    "username": "updated_admin",
    "email": "updated_admin@example.com"
}
```

---

## 2️⃣ DASHBOARD ANALYTICS

### 2.1 Get Dashboard Data
**GET** `/api/dashboard/`

**Response:**
```json
{
    "message": "Dashboard data retrieved successfully",
    "data": {
        "total_students": 150,
        "total_staff": 25,
        "total_departments": 5,
        "total_courses": 40,
        "upcoming_exams": 3,
        "attendance_overview": {
            "present": 0,
            "absent": 0,
            "percentage": 0
        },
        "result_summary": {
            "total": 120,
            "passed": 100,
            "failed": 20,
            "pass_percentage": 83.33
        }
    }
}
```

---

## 3️⃣ STUDENT MANAGEMENT

### 3.1 Create Student
**POST** `/api/students/`

**Request Body:**
```json
{
    "student_id": "STU001",
    "full_name": "John Doe",
    "register_no": "REG2024001",
    "department": 1,
    "year": 2,
    "semester": 3,
    "email": "john.doe@example.com",
    "phone": "9876543210",
    "address": "123 Main Street, City",
    "status": "active"
}
```

**Response:**
```json
{
    "message": "Student created successfully",
    "data": {
        "id": 1,
        "student_id": "STU001",
        "full_name": "John Doe",
        "register_no": "REG2024001",
        "department": 1,
        "department_name": "Computer Science",
        "year": 2,
        "semester": 3,
        "email": "john.doe@example.com",
        "phone": "9876543210",
        "address": "123 Main Street, City",
        "status": "active",
        "created_at": "2024-02-13T10:30:00Z",
        "updated_at": "2024-02-13T10:30:00Z"
    }
}
```

### 3.2 Get All Students (with pagination)
**GET** `/api/students/`

**Query Parameters:**
- `page=1`
- `department=1` (filter by department)
- `semester=3` (filter by semester)
- `search=John` (search by name)

**Response:**
```json
{
    "count": 150,
    "next": "http://localhost:8000/api/students/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "student_id": "STU001",
            "full_name": "John Doe",
            "register_no": "REG2024001",
            "department": 1,
            "department_name": "Computer Science",
            "year": 2,
            "semester": 3,
            "email": "john.doe@example.com",
            "phone": "9876543210",
            "address": "123 Main Street, City",
            "status": "active",
            "created_at": "2024-02-13T10:30:00Z",
            "updated_at": "2024-02-13T10:30:00Z"
        }
    ]
}
```

### 3.3 Get Single Student
**GET** `/api/students/1/`

### 3.4 Update Student
**PUT** `/api/students/1/`

**Request Body:**
```json
{
    "full_name": "John Doe Updated",
    "phone": "9876543211",
    "semester": 4
}
```

### 3.5 Delete Student (Soft Delete)
**DELETE** `/api/students/1/`

**Response:**
```json
{
    "message": "Student deleted successfully"
}
```

---

## 4️⃣ STAFF MANAGEMENT

### 4.1 Create Staff
**POST** `/api/staff/`

**Request Body:**
```json
{
    "staff_id": "STAFF001",
    "name": "Dr. Jane Smith",
    "email": "jane.smith@example.com",
    "phone": "9876543210",
    "department": 1,
    "designation": "Professor",
    "qualification": "PhD in Computer Science"
}
```

### 4.2 Get All Staff
**GET** `/api/staff/`

### 4.3 Get Single Staff
**GET** `/api/staff/1/`

### 4.4 Update Staff
**PUT** `/api/staff/1/`

### 4.5 Delete Staff
**DELETE** `/api/staff/1/`

---

## 5️⃣ DEPARTMENT MANAGEMENT

### 5.1 Create Department
**POST** `/api/departments/`

**Request Body:**
```json
{
    "department_name": "Computer Science",
    "department_code": "CSE",
    "hod": "Dr. Jane Smith",
    "description": "Department of Computer Science and Engineering"
}
```

**Response:**
```json
{
    "message": "Department created successfully",
    "data": {
        "id": 1,
        "department_name": "Computer Science",
        "department_code": "CSE",
        "hod": "Dr. Jane Smith",
        "description": "Department of Computer Science and Engineering",
        "total_students": 0,
        "total_staff": 0,
        "created_at": "2024-02-13T10:30:00Z",
        "updated_at": "2024-02-13T10:30:00Z"
    }
}
```

### 5.2 Get All Departments
**GET** `/api/departments/`

### 5.3 Get Single Department
**GET** `/api/departments/1/`

### 5.4 Update Department
**PUT** `/api/departments/1/`

### 5.5 Delete Department
**DELETE** `/api/departments/1/`

---

## 6️⃣ COURSE/SUBJECT MANAGEMENT

### 6.1 Create Course
**POST** `/api/courses/`

**Request Body:**
```json
{
    "course_code": "CS101",
    "course_name": "Data Structures",
    "department": 1,
    "credits": 4,
    "semester": 3,
    "assigned_faculty": 1
}
```

**Response:**
```json
{
    "message": "Course created successfully",
    "data": {
        "id": 1,
        "course_code": "CS101",
        "course_name": "Data Structures",
        "department": 1,
        "department_name": "Computer Science",
        "credits": 4,
        "semester": 3,
        "assigned_faculty": 1,
        "faculty_name": "Dr. Jane Smith",
        "created_at": "2024-02-13T10:30:00Z",
        "updated_at": "2024-02-13T10:30:00Z"
    }
}
```

### 6.2 Get All Courses
**GET** `/api/courses/`

**Query Parameters:**
- `department=1`
- `semester=3`
- `search=Data`

### 6.3 Get Single Course
**GET** `/api/courses/1/`

### 6.4 Update Course
**PUT** `/api/courses/1/`

### 6.5 Delete Course
**DELETE** `/api/courses/1/`

---

## 7️⃣ EXAM MANAGEMENT

### 7.1 Create Exam
**POST** `/api/exams/`

**Request Body:**
```json
{
    "exam_name": "Mid Semester Exam",
    "exam_type": "Internal",
    "start_date": "2024-03-01",
    "end_date": "2024-03-10",
    "duration": 180,
    "total_marks": 100,
    "semester": 3,
    "department": 1
}
```

**Response:**
```json
{
    "message": "Exam created successfully",
    "data": {
        "id": 1,
        "exam_name": "Mid Semester Exam",
        "exam_type": "Internal",
        "start_date": "2024-03-01",
        "end_date": "2024-03-10",
        "duration": 180,
        "total_marks": 100,
        "semester": 3,
        "department": 1,
        "department_name": "Computer Science",
        "created_at": "2024-02-13T10:30:00Z",
        "updated_at": "2024-02-13T10:30:00Z"
    }
}
```

### 7.2 Get All Exams
**GET** `/api/exams/`

**Query Parameters:**
- `exam_type=Internal`
- `semester=3`
- `department=1`

### 7.3 Get Single Exam
**GET** `/api/exams/1/`

### 7.4 Update Exam
**PUT** `/api/exams/1/`

### 7.5 Delete Exam
**DELETE** `/api/exams/1/`

---

## 8️⃣ EXAM SCHEDULE

### 8.1 Create Exam Schedule
**POST** `/api/exam-schedules/`

**Request Body:**
```json
{
    "exam": 1,
    "subject": 1,
    "date": "2024-03-01",
    "start_time": "09:00:00",
    "end_time": "12:00:00",
    "hall_number": "Hall-A101",
    "invigilator": 1
}
```

**Response:**
```json
{
    "message": "Exam schedule created successfully",
    "data": {
        "id": 1,
        "exam": 1,
        "exam_name": "Mid Semester Exam",
        "subject": 1,
        "subject_name": "Data Structures",
        "date": "2024-03-01",
        "start_time": "09:00:00",
        "end_time": "12:00:00",
        "hall_number": "Hall-A101",
        "invigilator": 1,
        "invigilator_name": "Dr. Jane Smith",
        "created_at": "2024-02-13T10:30:00Z",
        "updated_at": "2024-02-13T10:30:00Z"
    }
}
```

### 8.2 Get All Exam Schedules
**GET** `/api/exam-schedules/`

### 8.3 Get Single Exam Schedule
**GET** `/api/exam-schedules/1/`

### 8.4 Update Exam Schedule
**PUT** `/api/exam-schedules/1/`

### 8.5 Delete Exam Schedule
**DELETE** `/api/exam-schedules/1/`

---

## 9️⃣ HALL TICKET

### 9.1 Create Hall Ticket
**POST** `/api/hall-tickets/`

**Request Body:**
```json
{
    "student": 1,
    "exam": 1,
    "hall_ticket_number": "HT2024001"
}
```

**Response:**
```json
{
    "message": "Hall ticket created successfully",
    "data": {
        "id": 1,
        "student": 1,
        "student_name": "John Doe",
        "student_register_no": "REG2024001",
        "exam": 1,
        "exam_name": "Mid Semester Exam",
        "hall_ticket_number": "HT2024001",
        "issued_date": "2024-02-13",
        "qr_code": "/media/qr_codes/qr_HT2024001.png",
        "photo_url": null,
        "created_at": "2024-02-13T10:30:00Z"
    }
}
```

### 9.2 Get All Hall Tickets
**GET** `/api/hall-tickets/`

### 9.3 Get Hall Ticket by Student ID
**GET** `/api/hall-tickets/student/1/`

**Response:**
```json
{
    "message": "Hall tickets retrieved successfully",
    "data": [
        {
            "id": 1,
            "student": 1,
            "student_name": "John Doe",
            "student_register_no": "REG2024001",
            "exam": 1,
            "exam_name": "Mid Semester Exam",
            "hall_ticket_number": "HT2024001",
            "issued_date": "2024-02-13",
            "qr_code": "/media/qr_codes/qr_HT2024001.png",
            "photo_url": null,
            "created_at": "2024-02-13T10:30:00Z"
        }
    ]
}
```

### 9.4 Get Single Hall Ticket
**GET** `/api/hall-tickets/1/`

---

## 🔟 MARKS ENTRY

### 10.1 Create Marks Entry
**POST** `/api/marks/`

**Request Body:**
```json
{
    "student": 1,
    "subject": 1,
    "exam": 1,
    "internal_marks": 25,
    "external_marks": 70,
    "remarks": "Good performance"
}
```

**Response:**
```json
{
    "message": "Marks entry created successfully",
    "data": {
        "id": 1,
        "student": 1,
        "student_name": "John Doe",
        "subject": 1,
        "subject_name": "Data Structures",
        "exam": 1,
        "exam_name": "Mid Semester Exam",
        "internal_marks": 25,
        "external_marks": 70,
        "total_marks": 95,
        "grade": "O",
        "remarks": "Good performance",
        "created_at": "2024-02-13T10:30:00Z",
        "updated_at": "2024-02-13T10:30:00Z"
    }
}
```

### 10.2 Get All Marks
**GET** `/api/marks/`

**Query Parameters:**
- `student=1`
- `exam=1`
- `grade=O`

### 10.3 Get Single Marks Entry
**GET** `/api/marks/1/`

### 10.4 Update Marks Entry
**PUT** `/api/marks/1/`

**Request Body:**
```json
{
    "internal_marks": 28,
    "external_marks": 72
}
```

### 10.5 Delete Marks Entry
**DELETE** `/api/marks/1/`

---

## 1️⃣1️⃣ RESULTS PROCESSING

### 11.1 Create Result
**POST** `/api/results/`

**Request Body:**
```json
{
    "student": 1,
    "exam": 1,
    "total_marks": 450,
    "percentage": 90.00,
    "cgpa": 9.5,
    "result_status": "Pass"
}
```

**Response:**
```json
{
    "message": "Result created successfully",
    "data": {
        "id": 1,
        "student": 1,
        "student_name": "John Doe",
        "student_register_no": "REG2024001",
        "exam": 1,
        "exam_name": "Mid Semester Exam",
        "total_marks": 450,
        "percentage": "90.00",
        "cgpa": "9.50",
        "result_status": "Pass",
        "created_at": "2024-02-13T10:30:00Z",
        "updated_at": "2024-02-13T10:30:00Z"
    }
}
```

### 11.2 Get All Results
**GET** `/api/results/`

**Query Parameters:**
- `student=1`
- `exam=1`
- `result_status=Pass`

### 11.3 Get Result by Student ID
**GET** `/api/results/student/1/`

**Response:**
```json
{
    "message": "Results retrieved successfully",
    "data": [
        {
            "id": 1,
            "student": 1,
            "student_name": "John Doe",
            "student_register_no": "REG2024001",
            "exam": 1,
            "exam_name": "Mid Semester Exam",
            "total_marks": 450,
            "percentage": "90.00",
            "cgpa": "9.50",
            "result_status": "Pass",
            "created_at": "2024-02-13T10:30:00Z",
            "updated_at": "2024-02-13T10:30:00Z"
        }
    ]
}
```

### 11.4 Get Single Result
**GET** `/api/results/1/`

### 11.5 Update Result
**PUT** `/api/results/1/`

---

## 1️⃣2️⃣ NOTIFICATIONS

### 12.1 Create Notification
**POST** `/api/notifications/`

**Request Body:**
```json
{
    "title": "Exam Schedule Released",
    "message": "Mid semester exam schedule has been released. Please check your hall tickets.",
    "target_role": "Student"
}
```

**Response:**
```json
{
    "message": "Notification created successfully",
    "data": {
        "id": 1,
        "title": "Exam Schedule Released",
        "message": "Mid semester exam schedule has been released. Please check your hall tickets.",
        "target_role": "Student",
        "is_read": false,
        "created_at": "2024-02-13T10:30:00Z",
        "updated_at": "2024-02-13T10:30:00Z"
    }
}
```

### 12.2 Get All Notifications
**GET** `/api/notifications/`

**Query Parameters:**
- `target_role=Student`
- `is_read=false`

### 12.3 Get Single Notification
**GET** `/api/notifications/1/`

### 12.4 Update Notification (Mark as Read)
**PUT** `/api/notifications/1/`

**Request Body:**
```json
{
    "is_read": true
}
```

### 12.5 Delete Notification
**DELETE** `/api/notifications/1/`

---

## TESTING WORKFLOW IN POSTMAN

### Step 1: Register Admin User
```
POST /api/auth/register/
Body: {"username": "admin", "email": "admin@test.com", "password": "Admin@123", "role": "Admin"}
```

### Step 2: Login
```
POST /api/auth/login/
Body: {"email": "admin@test.com", "password": "Admin@123"}
Copy the access token from response
```

### Step 3: Set Authorization Header
```
In Postman, go to Authorization tab
Type: Bearer Token
Token: <paste your access token>
```

### Step 4: Test Each Module
1. Create Department
2. Create Staff
3. Create Student
4. Create Course
5. Create Exam
6. Create Exam Schedule
7. Create Hall Ticket
8. Create Marks Entry
9. Create Result
10. Create Notification
11. Test Dashboard API
12. Test all GET, PUT, DELETE operations

---

## ERROR RESPONSES

### 400 Bad Request
```json
{
    "message": "Validation failed",
    "errors": {
        "email": ["This field is required."]
    }
}
```

### 401 Unauthorized
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### 404 Not Found
```json
{
    "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
    "detail": "Internal server error"
}
```

---

## PAGINATION

All list APIs support pagination:
```
GET /api/students/?page=2&page_size=20
```

## FILTERING

```
GET /api/students/?department=1&semester=3&status=active
```

## SEARCHING

```
GET /api/students/?search=John
```

## ORDERING

```
GET /api/students/?ordering=-created_at
```
