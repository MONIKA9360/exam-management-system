# Exam Management System

Full Stack Exam Management System built with Django REST Framework and React.

## 🚀 Tech Stack

### Backend
- Django 4.x
- Django REST Framework
- MySQL Database
- JWT Authentication
- QR Code Generation

### Frontend
- React 18
- React Router DOM
- Axios
- Modern UI with Gradients

## 📋 Features

### 12 Complete Modules
1. **Authentication** - Login, Register, Profile Management
2. **Dashboard** - Analytics and Quick Search
3. **Departments** - Department Management
4. **Students** - Student Records Management
5. **Staff** - Staff Management
6. **Courses** - Course/Subject Management
7. **Exams** - Exam Creation and Management
8. **Exam Schedules** - Schedule Management with Clash Detection
9. **Hall Tickets** - Hall Ticket Generation with QR Codes
10. **Marks Entry** - Marks Entry with Auto Grade Calculation
11. **Results** - Result Processing and Publishing
12. **Notifications** - Role-based Notification System

### Key Features
- ✅ JWT Token Authentication
- ✅ Role-Based Access Control (Admin, Staff, Student)
- ✅ Soft Delete Implementation
- ✅ Audit Logging
- ✅ Search Functionality
- ✅ Pagination & Filtering
- ✅ Beautiful Gradient UI
- ✅ Responsive Design
- ✅ Form Validation
- ✅ QR Code Generation for Hall Tickets

## 🛠️ Setup Instructions

### Backend Setup

1. Navigate to backend folder:
```bash
cd backend/Exam_management
```

2. Create virtual environment:
```bash
python -m venv env
env\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure MySQL database in `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'examination',
        'USER': 'root',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

5. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create superuser:
```bash
python manage.py createsuperuser
```

7. Run server:
```bash
python manage.py runserver
```

Backend will run at: `http://127.0.0.1:8000/`

### Frontend Setup

1. Navigate to frontend folder:
```bash
cd my-app
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm start
```

Frontend will run at: `http://localhost:3000/`

## 📡 API Endpoints

### Authentication
- POST `/api/auth/register/` - User Registration
- POST `/api/auth/login/` - User Login
- GET `/api/auth/profile/` - Get User Profile
- PUT `/api/auth/profile/update/` - Update Profile

### Dashboard
- GET `/api/dashboard/` - Get Dashboard Statistics

### Departments
- GET `/api/departments/` - List all departments
- POST `/api/departments/` - Create department
- GET `/api/departments/{id}/` - Get department details
- PUT `/api/departments/{id}/` - Update department
- DELETE `/api/departments/{id}/` - Delete department

### Students
- GET `/api/students/` - List all students
- POST `/api/students/` - Create student
- GET `/api/students/{id}/` - Get student details
- PUT `/api/students/{id}/` - Update student
- DELETE `/api/students/{id}/` - Delete student

### Staff
- GET `/api/staff/` - List all staff
- POST `/api/staff/` - Create staff
- GET `/api/staff/{id}/` - Get staff details
- PUT `/api/staff/{id}/` - Update staff
- DELETE `/api/staff/{id}/` - Delete staff

### Courses
- GET `/api/courses/` - List all courses
- POST `/api/courses/` - Create course
- GET `/api/courses/{id}/` - Get course details
- PUT `/api/courses/{id}/` - Update course
- DELETE `/api/courses/{id}/` - Delete course

### Exams
- GET `/api/exams/` - List all exams
- POST `/api/exams/` - Create exam
- GET `/api/exams/{id}/` - Get exam details
- PUT `/api/exams/{id}/` - Update exam
- DELETE `/api/exams/{id}/` - Delete exam

### Exam Schedules
- GET `/api/exam-schedules/` - List all schedules
- POST `/api/exam-schedules/` - Create schedule
- GET `/api/exam-schedules/{id}/` - Get schedule details
- PUT `/api/exam-schedules/{id}/` - Update schedule
- DELETE `/api/exam-schedules/{id}/` - Delete schedule

### Hall Tickets
- GET `/api/hall-tickets/` - List all hall tickets
- POST `/api/hall-tickets/` - Generate hall ticket
- GET `/api/hall-tickets/{id}/` - Get hall ticket details
- GET `/api/hall-tickets/student/{id}/` - Get student's hall tickets

### Marks Entry
- GET `/api/marks/` - List all marks
- POST `/api/marks/` - Enter marks
- GET `/api/marks/{id}/` - Get marks details
- PUT `/api/marks/{id}/` - Update marks
- DELETE `/api/marks/{id}/` - Delete marks

### Results
- GET `/api/results/` - List all results
- POST `/api/results/` - Create result
- GET `/api/results/{id}/` - Get result details
- GET `/api/results/student/{id}/` - Get student's results
- PUT `/api/results/{id}/` - Update result

### Notifications
- GET `/api/notifications/` - List all notifications
- POST `/api/notifications/` - Create notification
- GET `/api/notifications/{id}/` - Get notification details
- PUT `/api/notifications/{id}/` - Update notification
- DELETE `/api/notifications/{id}/` - Delete notification

## 🔐 Authentication

All API endpoints (except register and login) require JWT authentication.

Include the token in the Authorization header:
```
Authorization: Bearer <your_access_token>
```

## 👤 Default Credentials

After running migrations, you can create a superuser or register through the UI.

## 📸 Screenshots

(Add screenshots of your application here)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.

## 👨‍💻 Developer

**MONIKA M**
- GitHub: [@MONIKA9360](https://github.com/MONIKA9360)

## 🙏 Acknowledgments

- Django REST Framework Documentation
- React Documentation
- Material Design Guidelines
