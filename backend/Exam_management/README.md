# EXAM MANAGEMENT SYSTEM - BACKEND

A complete, production-ready Django REST Framework backend for managing educational institution exams, students, staff, and results.

## 🚀 Features

### Core Modules (12 Complete Modules)
1. **Authentication & Role Management** - JWT-based auth with Admin/Staff/Student roles
2. **Dashboard Analytics** - Real-time statistics and insights
3. **Student Management** - Complete student lifecycle management
4. **Staff Management** - Faculty and staff administration
5. **Department Management** - Academic department organization
6. **Course/Subject Management** - Course catalog and assignments
7. **Exam Management** - Exam scheduling and configuration
8. **Exam Schedule** - Detailed exam timetables with clash detection
9. **Hall Ticket** - Automated hall ticket generation with QR codes
10. **Marks Entry** - Grade management with auto-calculation
11. **Results Processing** - Result computation with CGPA/percentage
12. **Notifications** - Role-based notification system

### Technical Features
- ✅ Custom User Model with Role-Based Access Control (RBAC)
- ✅ JWT Authentication (SimpleJWT)
- ✅ MySQL Database Integration
- ✅ RESTful API with ViewSets & Routers
- ✅ Pagination, Filtering & Search
- ✅ Soft Delete Functionality
- ✅ Audit Logging System
- ✅ Automatic Timestamps (created_at, updated_at)
- ✅ Data Validation & Error Handling
- ✅ CORS Enabled for Frontend Integration
- ✅ QR Code Generation
- ✅ Admin Panel Integration

## 📋 Tech Stack

- **Backend Framework:** Django 4.2.7
- **API Framework:** Django REST Framework 3.14.0
- **Authentication:** djangorestframework-simplejwt 5.3.0
- **Database:** MySQL 8.0+ (mysqlclient 2.2.0)
- **CORS:** django-cors-headers 4.3.0
- **Filtering:** django-filter 23.3
- **QR Codes:** qrcode 7.4.2
- **Image Processing:** Pillow 10.1.0

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- MySQL Server 8.0+
- pip package manager

### Quick Start

1. **Clone and Navigate**
```bash
cd backend/Exam_management
```

2. **Create Virtual Environment**
```bash
python -m venv env
env\Scripts\activate  # Windows
source env/bin/activate  # Linux/Mac
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure MySQL**
```sql
CREATE DATABASE examination CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Update credentials in `Exam_management/settings.py` if needed.

5. **Run Migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create Superuser**
```bash
python manage.py createsuperuser
```

7. **Start Server**
```bash
python manage.py runserver
```

Server runs at: `http://127.0.0.1:8000/`

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api/
```

### Authentication
All APIs (except register/login) require JWT token:
```
Authorization: Bearer <access_token>
```

### API Endpoints

#### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login and get JWT tokens
- `GET /api/auth/profile/` - Get user profile
- `PUT /api/auth/profile/update/` - Update profile

#### Dashboard
- `GET /api/dashboard/` - Get analytics data

#### Students
- `GET /api/students/` - List all students (paginated)
- `POST /api/students/` - Create student
- `GET /api/students/{id}/` - Get student details
- `PUT /api/students/{id}/` - Update student
- `DELETE /api/students/{id}/` - Delete student (soft)

#### Staff
- `GET /api/staff/` - List all staff
- `POST /api/staff/` - Create staff
- `GET /api/staff/{id}/` - Get staff details
- `PUT /api/staff/{id}/` - Update staff
- `DELETE /api/staff/{id}/` - Delete staff

#### Departments
- `GET /api/departments/` - List all departments
- `POST /api/departments/` - Create department
- `GET /api/departments/{id}/` - Get department details
- `PUT /api/departments/{id}/` - Update department
- `DELETE /api/departments/{id}/` - Delete department

#### Courses
- `GET /api/courses/` - List all courses
- `POST /api/courses/` - Create course
- `GET /api/courses/{id}/` - Get course details
- `PUT /api/courses/{id}/` - Update course
- `DELETE /api/courses/{id}/` - Delete course

#### Exams
- `GET /api/exams/` - List all exams
- `POST /api/exams/` - Create exam
- `GET /api/exams/{id}/` - Get exam details
- `PUT /api/exams/{id}/` - Update exam
- `DELETE /api/exams/{id}/` - Delete exam

#### Exam Schedules
- `GET /api/exam-schedules/` - List all schedules
- `POST /api/exam-schedules/` - Create schedule
- `GET /api/exam-schedules/{id}/` - Get schedule details
- `PUT /api/exam-schedules/{id}/` - Update schedule
- `DELETE /api/exam-schedules/{id}/` - Delete schedule

#### Hall Tickets
- `GET /api/hall-tickets/` - List all hall tickets
- `POST /api/hall-tickets/` - Create hall ticket
- `GET /api/hall-tickets/student/{student_id}/` - Get by student
- `GET /api/hall-tickets/{id}/` - Get hall ticket details

#### Marks
- `GET /api/marks/` - List all marks
- `POST /api/marks/` - Create marks entry
- `GET /api/marks/{id}/` - Get marks details
- `PUT /api/marks/{id}/` - Update marks
- `DELETE /api/marks/{id}/` - Delete marks

#### Results
- `GET /api/results/` - List all results
- `POST /api/results/` - Create result
- `GET /api/results/student/{student_id}/` - Get by student
- `GET /api/results/{id}/` - Get result details
- `PUT /api/results/{id}/` - Update result

#### Notifications
- `GET /api/notifications/` - List notifications (role-filtered)
- `POST /api/notifications/` - Create notification
- `GET /api/notifications/{id}/` - Get notification details
- `PUT /api/notifications/{id}/` - Update notification
- `DELETE /api/notifications/{id}/` - Delete notification

### Query Parameters

**Pagination:**
```
?page=1&page_size=10
```

**Filtering:**
```
?department=1&semester=3&status=active
```

**Search:**
```
?search=John
```

**Ordering:**
```
?ordering=-created_at
```

## 🧪 Testing in Postman

See `POSTMAN_API_GUIDE.md` for complete API testing guide with sample requests and responses.

### Quick Test Flow:
1. Register admin user
2. Login and get access token
3. Set Bearer token in Authorization header
4. Test each module's CRUD operations
5. Verify pagination, filtering, and search
6. Check audit logs in admin panel

## 📁 Project Structure

```
backend/Exam_management/
├── Exam_management/          # Project settings
│   ├── settings.py          # Configuration
│   ├── urls.py              # Main URL routing
│   └── wsgi.py              # WSGI config
├── myapp/                   # Main application
│   ├── models.py            # Database models (12 modules)
│   ├── serializers.py       # DRF serializers
│   ├── views.py             # API views & viewsets
│   ├── urls.py              # App URL routing
│   ├── admin.py             # Admin panel config
│   └── permissions.py       # Custom permissions
├── media/                   # Uploaded files
├── manage.py                # Django CLI
├── requirements.txt         # Dependencies
├── README.md                # This file
├── SETUP_INSTRUCTIONS.md    # Detailed setup guide
└── POSTMAN_API_GUIDE.md     # API documentation
```

## 🔐 Security Features

- JWT token-based authentication
- Role-based access control (Admin/Staff/Student)
- Password hashing with Django's built-in system
- CSRF protection
- SQL injection prevention (Django ORM)
- XSS protection
- Audit logging for all operations

## 📊 Database Schema

### Core Tables
- `users` - Custom user model with roles
- `students` - Student information
- `staff` - Staff/faculty information
- `departments` - Academic departments
- `courses` - Course/subject catalog
- `exams` - Exam configurations
- `exam_schedules` - Detailed exam timetables
- `hall_tickets` - Hall ticket records
- `marks_entries` - Student marks
- `results` - Processed results
- `notifications` - System notifications
- `audit_logs` - Activity tracking

## 🎯 Key Features Explained

### Soft Delete
All models support soft delete - records are marked as deleted but not removed from database.

### Audit Logging
Every create, update, delete operation is logged with:
- User who performed action
- Action type
- Model name
- Changes made
- IP address
- Timestamp

### Auto-Calculations
- **Marks Entry:** Total marks and grades calculated automatically
- **Results:** Percentage and CGPA computed from marks
- **Dashboard:** Real-time statistics aggregated from database

### Validation
- Email uniqueness checks
- Register number uniqueness
- Course code uniqueness
- Marks cannot exceed exam total
- Exam end date must be after start date
- Hall clash detection in schedules

## 🚀 Production Deployment

Before deploying:
1. Set `DEBUG = False`
2. Update `SECRET_KEY`
3. Configure `ALLOWED_HOSTS`
4. Set up proper database credentials
5. Configure static files serving (WhiteNoise/Nginx)
6. Set up HTTPS
7. Configure email backend
8. Set up logging and monitoring
9. Configure backup strategy

## 📝 License

This project is for educational purposes.

## 👨‍💻 Development

**Status:** ✅ Complete and Production-Ready

All 12 modules are fully implemented with:
- Complete CRUD operations
- Proper validation
- Error handling
- Pagination and filtering
- Role-based permissions
- Audit logging
- Admin panel integration

Ready for frontend integration and Postman testing!

## 📞 Support

For detailed setup instructions, see `SETUP_INSTRUCTIONS.md`
For API testing guide, see `POSTMAN_API_GUIDE.md`

---

**Built with Django REST Framework** 🎓
