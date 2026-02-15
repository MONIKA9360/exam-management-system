# QUICK START GUIDE - EXAM MANAGEMENT SYSTEM

## ⚡ 5-Minute Setup

### 1. Install Dependencies (1 min)
```bash
cd backend/Exam_management
pip install -r requirements.txt
```

### 2. Create MySQL Database (1 min)
```sql
CREATE DATABASE examination;
```

### 3. Run Migrations (1 min)
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Admin User (1 min)
```bash
python manage.py createsuperuser
# Email: admin@test.com
# Username: admin
# Password: Admin@123
```

### 5. Start Server (1 min)
```bash
python manage.py runserver
```

✅ Server running at: http://127.0.0.1:8000/

---

## 🚀 Test in Postman (5 minutes)

### Step 1: Register User
```
POST http://127.0.0.1:8000/api/auth/register/
Body: {
    "username": "testadmin",
    "email": "test@example.com",
    "password": "Test@123",
    "role": "Admin"
}
```

### Step 2: Login & Get Token
```
POST http://127.0.0.1:8000/api/auth/login/
Body: {
    "email": "test@example.com",
    "password": "Test@123"
}
```
**Copy the access_token from response!**

### Step 3: Set Authorization
```
Authorization: Bearer <your_access_token>
```

### Step 4: Test Dashboard
```
GET http://127.0.0.1:8000/api/dashboard/
```

### Step 5: Create Department
```
POST http://127.0.0.1:8000/api/departments/
Body: {
    "department_name": "Computer Science",
    "department_code": "CSE",
    "hod": "Dr. Smith"
}
```

### Step 6: Create Student
```
POST http://127.0.0.1:8000/api/students/
Body: {
    "student_id": "STU001",
    "full_name": "John Doe",
    "register_no": "REG001",
    "department": 1,
    "year": 2,
    "semester": 3,
    "email": "john@test.com",
    "phone": "1234567890",
    "address": "Test Address",
    "status": "active"
}
```

---

## 📋 All API Endpoints

### Authentication
- POST `/api/auth/register/` - Register
- POST `/api/auth/login/` - Login
- GET `/api/auth/profile/` - Get Profile
- PUT `/api/auth/profile/update/` - Update Profile

### Dashboard
- GET `/api/dashboard/` - Analytics

### CRUD Endpoints (All follow same pattern)
- GET `/api/{module}/` - List all
- POST `/api/{module}/` - Create
- GET `/api/{module}/{id}/` - Get one
- PUT `/api/{module}/{id}/` - Update
- DELETE `/api/{module}/{id}/` - Delete

### Modules:
- `/api/students/`
- `/api/staff/`
- `/api/departments/`
- `/api/courses/`
- `/api/exams/`
- `/api/exam-schedules/`
- `/api/hall-tickets/`
- `/api/marks/`
- `/api/results/`
- `/api/notifications/`

### Special Endpoints:
- GET `/api/hall-tickets/student/{id}/` - Hall tickets by student
- GET `/api/results/student/{id}/` - Results by student

---

## 🎯 Testing Order

1. ✅ Register & Login
2. ✅ Create Department
3. ✅ Create Staff
4. ✅ Create Student
5. ✅ Create Course
6. ✅ Create Exam
7. ✅ Create Exam Schedule
8. ✅ Create Hall Ticket
9. ✅ Create Marks Entry
10. ✅ Create Result
11. ✅ Create Notification
12. ✅ Test Dashboard

---

## 📦 Import Postman Collection

1. Open Postman
2. Click Import
3. Select `Postman_Collection.json`
4. Set `access_token` variable after login
5. Test all endpoints!

---

## 🔧 Troubleshooting

**MySQL Error?**
```bash
# Check MySQL is running
# Verify credentials in settings.py
```

**Module Not Found?**
```bash
pip install -r requirements.txt
```

**Migration Error?**
```bash
python manage.py migrate --run-syncdb
```

---

## 📚 Documentation Files

- `README.md` - Project overview
- `SETUP_INSTRUCTIONS.md` - Detailed setup
- `POSTMAN_API_GUIDE.md` - Complete API docs
- `Postman_Collection.json` - Import to Postman
- `QUICK_START.md` - This file

---

## ✅ Features Checklist

- [x] 12 Complete Modules
- [x] JWT Authentication
- [x] Role-Based Access Control
- [x] Pagination & Filtering
- [x] Search Functionality
- [x] Soft Delete
- [x] Audit Logs
- [x] Auto Calculations
- [x] QR Code Generation
- [x] MySQL Integration
- [x] CORS Enabled
- [x] Admin Panel

---

**Backend is 100% Complete and Ready! 🎉**

Test all 12 modules in Postman now!
