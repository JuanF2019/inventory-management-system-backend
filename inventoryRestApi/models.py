from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from datetime import datetime


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100)


class InventoryProduct(models.Model):
    code = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    dimensions = models.CharField(max_length=100, null=True, blank=True)
    cost = models.DecimalField(decimal_places=2, max_digits=20)
    sellingPrice = models.DecimalField(decimal_places=2, max_digits=20)
    unitsAvailable = models.IntegerField(null=False, blank=False, default=0)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)

    def __str__(self):
        return self.code + ", " + self.name + ", " + str(self.unitsAvailable)


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, document, doc_type, first_name, last_name, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        if not password:
            raise ValueError('Email is required')
        if not document:
            raise ValueError('Document is required')
        if not doc_type:
            raise ValueError('Doc_type is required')
        if not first_name:
            raise ValueError('first_name is required')
        if not doc_type:
            raise ValueError('last_name is required')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.document = document
        user.doc_type = doc_type
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return user

    def create_superuser(self, email, password, document, doc_type, first_name, last_name, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')

        return self.create_user(email, password, document, doc_type, first_name, last_name, **extra_fields)


class User(AbstractUser):
    DOCUMENT_TYPES = [
        ('CC', 'CC'),
        ('TI', 'TI'),
        ('RC', 'RC'),
        ('NUIP', 'NUIP'),
        ('CE', 'CE'),
        ('PS', 'PS'),
        ('NIP', 'NIP'),
        ('NES', 'NES'),
    ]

    # first and last name are inherited from abstract user
    username = None
    USERNAME_FIELD = 'email'
    email = models.EmailField(max_length=100, unique=True)

    document = models.CharField(max_length=10, primary_key=True)
    doc_type = models.CharField(max_length=4, choices=DOCUMENT_TYPES)
    phone_number = models.CharField(max_length=15, null=True)
    birthday = models.DateField(null=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    first_name = models.CharField(("first name"), max_length=150)
    last_name = models.CharField(("last name"), max_length=150)

    REQUIRED_FIELDS = ['first_name', 'document', 'doc_type']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name}, {self.last_name}"


class InventoryMovement(models.Model):
    MOV_TYPES = [
        ('Entrada', 'Entrada'),
        ('Salida', 'Salida')
    ]
    product = models.ForeignKey(InventoryProduct, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    date = models.DateTimeField()
    description = models.TextField()
    units = models.PositiveIntegerField()
    movType = models.CharField(max_length=20, choices=MOV_TYPES)
