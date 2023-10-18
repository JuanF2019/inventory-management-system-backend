import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventoryProj.settings')

import django
from django.contrib.auth.models import Group

GROUPS = ['admin','warehouse_keeper']
MODELS = ['user']

for group in Groups:
    new_group, created = Group.objects.get_or_create(name=group)