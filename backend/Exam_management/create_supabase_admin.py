import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Exam_management.settings')
django.setup()

from myapp.models import User

# Create admin user
email = "admin@college.edu"
username = "admin"
password = "admin123"

# Check if user exists
existing_user = User.objects.filter(email=email).first()

if existing_user:
    print(f"✓ Admin user already exists!")
    print(f"  Email: {existing_user.email}")
else:
    user = User.objects.create_user(
        email=email,
        username=username,
        password=password
    )
    user.role = 'Admin'
    user.is_active = True
    user.is_staff = True
    user.is_superuser = True
    user.save()
    print(f"✓ Admin user created successfully!")

print(f"\n{'='*50}")
print(f"Supabase PostgreSQL Connected!")
print(f"{'='*50}")
print(f"Login Credentials:")
print(f"Email:    {email}")
print(f"Password: {password}")
print(f"{'='*50}")
