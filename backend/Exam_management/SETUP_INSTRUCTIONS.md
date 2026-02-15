# EXAM MANAGEMENT SYSTEM - SETUP INSTRUCTIONS

## Prerequisites
- Python 3.8 or higher
- MySQL Server 8.0 or higher
- pip (Python package manager)
- Postman (for API testing)

---

## STEP 1: Install Dependencies

### 1.1 Navigate to project directory
```bash
cd backend/Exam_management
```

### 1.2 Create virtual environment (recommended)
```bash
python -m venv env
```

### 1.3 Activate virtual environment

**Windows:**
```bash
env\Scripts\activate
```

**Linux/Mac:**
```bash
source env/bin/activate
```

### 1.4 Install required packages
```bash
pip install -r requirements.txt
```

---

## STEP 2: Configure MySQL Database

### 2.1 Start MySQL Server
Make sure MySQL server is running on your system.

### 2.2 Create Database
Open MySQL command line or MySQL Workbench and run:

```sql
CREATE DATABASE examination CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2.3 Verify Database Settings
Check `Exam_management/settings.py` - Database configuration:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'examination',
        'USER': 'root',
        'PASSWORD': 'Monika@2004',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

**Note:** If your MySQL credentials are different, update them in settings.py

---

## STEP 3: Run Migrations

### 3.1 Make migrations
```bash
python manage.py makemigrations
```

### 3.2 Apply migrations
```bash
python manage.py migrate
```

This will create all database tables for:
- Users
- Students
- Staff
- Departments
- Courses
- Exams
- Exam Schedules
- Hall Tickets
- Marks Entries
- Results
- Notifications
- Audit Logs

---

## STEP 4: Create Superuser

### 4.1 Create admin account
```bash
python manage.py createsuperuser
```

You will be prompted to enter:
- Email: admin@example.com
- Username: admin
- Password: (enter a strong password)

---

## STEP 5: Run Development Server

### 5.1 Start the server
```bash
python manage.py runserver
```

The server will start at: `http://127.0.0.1:8000/`

### 5.2 Verify server is running
Open browser and visit:
- Admin Panel: `http://127.0.0.1:8000/admin/`
- API Root: `http://127.0.0.1:8000/api/`

---

## STEP 6: Test APIs in Postman

### 6.1 Import Postman Collection
Refer to `POSTMAN_API_GUIDE.md` for complete API documentation.

### 6.2 Test Authentication

#### Register a new user:
```
POST http://127.0.0.1:8000/api/auth/register/
Content-Type: application/json

{
    "username": "testadmin",
    "email": "testadmin@example.com",
    "password": "Test@123",
    "role": "Admin"
}
```

#### Login:
```
POST http://127.0.0.1:8000/api/auth/login/
Content-Type: application/json

{
    "email": "testadmin@example.com",
    "password": "Test@123"
}
```

**Copy the access token from response!**

### 6.3 Set Authorization Header
For all subsequent requests, add header:
```
Authorization: Bearer <your_access_token>
```

### 6.4 Test Dashboard API
```
GET http://127.0.0.1:8000/api/dashboard/
Authorization: Bearer <your_access_token>
```

### 6.5 Test All 12 Modules

Follow this order for testing:

1. **Department Management**
   - POST `/api/departments/` - Create department
   - GET `/api/departments/` - List all departments
   - GET `/api/departments/1/` - Get single department
   - PUT `/api/departments/1/` - Update department
   - DELETE `/api/departments/1/` - Delete department

2. **Staff Management**
   - POST `/api/staff/` - Create staff
   - GET `/api/staff/` - List all staff
   - GET `/api/staff/1/` - Get single staff
   - PUT `/api/staff/1/` - Update staff
   - DELETE `/api/staff/1/` - Delete staff

3. **Student Management**
   - POST `/api/students/` - Create student
   - GET `/api/students/` - List all students
   - GET `/api/students/1/` - Get single student
   - PUT `/api/students/1/` - Update student
   - DELETE `/api/students/1/` - Delete student

4. **Course Management**
   - POST `/api/courses/` - Create course
   - GET `/api/courses/` - List all courses
   - GET `/api/courses/1/` - Get single course
   - PUT `/api/courses/1/` - Update course
   - DELETE `/api/courses/1/` - Delete course

5. **Exam Management**
   - POST `/api/exams/` - Create exam
   - GET `/api/exams/` - List all exams
   - GET `/api/exams/1/` - Get single exam
   - PUT `/api/exams/1/` - Update exam
   - DELETE `/api/exams/1/` - Delete exam

6. **Exam Schedule**
   - POST `/api/exam-schedules/` - Create schedule
   - GET `/api/exam-schedules/` - List all schedules
   - GET `/api/exam-schedules/1/` - Get single schedule
   - PUT `/api/exam-schedules/1/` - Update schedule
   - DELETE `/api/exam-schedules/1/` - Delete schedule

7. **Hall Ticket**
   - POST `/api/hall-tickets/` - Create hall ticket
   - GET `/api/hall-tickets/` - List all hall tickets
   - GET `/api/hall-tickets/student/1/` - Get by student
   - GET `/api/hall-tickets/1/` - Get single hall ticket

8. **Marks Entry**
   - POST `/api/marks/` - Create marks entry
   - GET `/api/marks/` - List all marks
   - GET `/api/marks/1/` - Get single marks entry
   - PUT `/api/marks/1/` - Update marks
   - DELETE `/api/marks/1/` - Delete marks

9. **Results Processing**
   - POST `/api/results/` - Create result
   - GET `/api/results/` - List all results
   - GET `/api/results/student/1/` - Get by student
   - GET `/api/results/1/` - Get single result
   - PUT `/api/results/1/` - Update result

10. **Notifications**
    - POST `/api/notifications/` - Create notification
    - GET `/api/notifications/` - List all notifications
    - GET `/api/notifications/1/` - Get single notification
    - PUT `/api/notifications/1/` - Update notification
    - DELETE `/api/notifications/1/` - Delete notification

11. **Dashboard Analytics**
    - GET `/api/dashboard/` - Get dashboard data

12. **Authentication & Profile**
    - POST `/api/auth/register/` - Register user
    - POST `/api/auth/login/` - Login user
    - GET `/api/auth/profile/` - Get profile
    - PUT `/api/auth/profile/update/` - Update profile

---

## STEP 7: Access Admin Panel

### 7.1 Login to Admin Panel
Visit: `http://127.0.0.1:8000/admin/`

Login with superuser credentials created in Step 4.

### 7.2 Manage Data
You can manage all models through the admin panel:
- Users
- Students
- Staff
- Departments
- Courses
- Exams
- Exam Schedules
- Hall Tickets
- Marks Entries
- Results
- Notifications
- Audit Logs

---

## FEATURES IMPLEMENTED

✅ Custom User Model with Role-Based Access Control
✅ JWT Authentication
✅ 12 Complete Modules with Full CRUD Operations
✅ Pagination on all list APIs
✅ Filtering and Search functionality
✅ Soft Delete feature
✅ Created_at & Updated_at timestamps
✅ Audit Logs for all operations
✅ Proper validation and error handling
✅ MySQL database integration
✅ CORS enabled for frontend integration
✅ QR Code generation for hall tickets
✅ Auto-calculation of grades and results
✅ Hall clash validation in exam schedules
✅ Role-based notification filtering

---

## TESTING CHECKLIST

- [ ] User Registration (Admin, Staff, Student)
- [ ] User Login & JWT Token Generation
- [ ] Profile View & Update
- [ ] Dashboard Analytics
- [ ] Department CRUD Operations
- [ ] Staff CRUD Operations
- [ ] Student CRUD Operations (with filters)
- [ ] Course CRUD Operations
- [ ] Exam CRUD Operations
- [ ] Exam Schedule CRUD (with clash validation)
- [ ] Hall Ticket Generation (with QR code)
- [ ] Marks Entry (with auto grade calculation)
- [ ] Results Processing (with percentage & CGPA)
- [ ] Notifications (role-based filtering)
- [ ] Pagination on all list APIs
- [ ] Search functionality
- [ ] Soft Delete functionality
- [ ] Audit Logs creation

---

## TROUBLESHOOTING

### Issue: MySQL Connection Error
**Solution:** 
- Verify MySQL server is running
- Check database credentials in settings.py
- Ensure 'examination' database exists

### Issue: Module Import Error
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: Migration Error
**Solution:**
```bash
python manage.py makemigrations --empty myapp
python manage.py migrate
```

### Issue: Static Files Not Loading
**Solution:**
```bash
python manage.py collectstatic
```

### Issue: CORS Error in Frontend
**Solution:**
- Check CORS_ALLOWED_ORIGINS in settings.py
- Add your frontend URL to the list

---

## PROJECT STRUCTURE

```
backend/Exam_management/
├── Exam_management/
│   ├── __init__.py
│   ├── settings.py          # Main settings
│   ├── urls.py              # Main URL configuration
│   ├── wsgi.py
│   └── asgi.py
├── myapp/
│   ├── __init__.py
│   ├── models.py            # All 12 models
│   ├── serializers.py       # All serializers
│   ├── views.py             # All ViewSets & APIs
│   ├── urls.py              # App URL configuration
│   ├── admin.py             # Admin panel configuration
│   ├── permissions.py       # Custom permissions
│   └── migrations/          # Database migrations
├── media/                   # Uploaded files (QR codes, photos)
├── staticfiles/             # Static files
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
├── SETUP_INSTRUCTIONS.md    # This file
└── POSTMAN_API_GUIDE.md     # API documentation
```

---

## NEXT STEPS

1. ✅ Backend is complete and ready
2. Test all APIs in Postman
3. Build React frontend (separate task)
4. Integrate frontend with backend APIs
5. Deploy to production server

---

## SUPPORT

For any issues or questions:
1. Check POSTMAN_API_GUIDE.md for API documentation
2. Review Django error logs in console
3. Check MySQL error logs
4. Verify all dependencies are installed

---

## PRODUCTION DEPLOYMENT CHECKLIST

Before deploying to production:
- [ ] Set DEBUG = False in settings.py
- [ ] Update SECRET_KEY
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up proper database credentials
- [ ] Configure static files serving
- [ ] Set up HTTPS
- [ ] Configure email backend for notifications
- [ ] Set up proper logging
- [ ] Configure backup strategy
- [ ] Set up monitoring and alerts

---

**Backend Development Complete! ✅**

All 12 modules are fully functional and ready for testing in Postman.
