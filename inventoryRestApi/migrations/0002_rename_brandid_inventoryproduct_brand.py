# Generated by Django 4.2.6 on 2023-10-11 13:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventoryRestApi', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inventoryproduct',
            old_name='brandId',
            new_name='brand',
        ),
    ]