import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Create superuser if it doesn't exist
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123'  # CHANGE THIS IMMEDIATELY AFTER FIRST LOGIN!
    )
    print("✅ Superuser 'admin' created successfully!")
    print("⚠️  Username: admin")
    print("⚠️  Password: admin123")
    print("⚠️  PLEASE CHANGE PASSWORD IMMEDIATELY AFTER LOGIN!")
else:
    print("✅ Superuser already exists.")
