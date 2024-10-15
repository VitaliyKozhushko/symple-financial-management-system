"""
Создание суперпользователя
"""
import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fms.settings')

django.setup()

User = get_user_model()

if not User.objects.filter(email='admin@example.com').exists():
    User.objects.create_superuser(
        email='admin@example.com',
        first_name='Admin',
        last_name='User',
        password='admin'
    )
    print('Superuser admin created.')
else:
    print('Superuser admin already exists.')
