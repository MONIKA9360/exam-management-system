import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Exam_management.settings')
django.setup()

from myapp.models import User

# Create admin user
admin_email = 'admin@college.edu'
admin_username = 'admin'
admin_password = 'admin123'

# Check if admin already exists
if User.objects.filter(email=admin_email).exists():
    print(f"✓ Admin user already exists: {admin_email}")
    admin = User.objects.get(email=admin_email)
    # Update password
    admin.set_password(admin_password)
    admin.role = 'Admin'
    admin.is_staff = True
    admin.is_superuser = True
    admin.save()
    print(f"✓ Admin password updated")
else:
    # Create new admin
    admin = User.objects.create_user(
        email=admin_email,
        username=admin_username,
        password=admin_password,
        role='Admin',
        is_staff=True,
        is_superuser=True
    )
    print(f"✓ Admin user created: {admin_email}")

print("\n" + "="*50)
print("ADMIN LOGIN CREDENTIALS")
print("="*50)
print(f"Email: {admin_email}")
print(f"Password: {admin_password}")
print("="*50)
