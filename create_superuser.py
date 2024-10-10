import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'airspace_restriction_zones.settings')

django.setup()

User = get_user_model()

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(username='admin', email='admin@example.com', password='admin')
    print(f'Superuser admin created.')
else:
    print(f'Superuser admin already exists.')
