from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group, PermissionsMixin, AbstractUser

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

class Brand(models.Model):
    name = models.CharField(max_length=100)

class InventoryProduct(models.Model):
    code = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    dimensions = models.CharField(max_length=100, null=True, blank=True)
    cost = models.DecimalField(decimal_places=2, max_digits=20)
    sellingPrice = models.DecimalField(decimal_places=2, max_digits=20)
    unitsAvailable = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError('Email is required')
        user = self.model(email=self.normalize_email(email),**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
    
    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser,PermissionsMixin):
    username = None
    DOCUMENT_TYPES = [
        ('CC','CC'),
        ('TI','TI'),  
        ('RC','RC'),
        ('NUIP','NUIP'),
        ('CE','CE'),
        ('PS','PS'),       
        ('NIP','NIP'),
        ('NES','NES'),
    ]
    #first and last name are inherited from abstrac user
    document = models.CharField(max_length=10,null=True)
    docType = models.CharField(max_length=4, choices=DOCUMENT_TYPES,null=True)
    email = models.EmailField(max_length=100, unique=True)
    phoneNumber = models.CharField(max_length=15,null=True)
    birthday = models.DateField(null=True)
    
    #This is just for following the guide on authentication
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    def __str__(self):
        return self.first_name

class InventoryMovement(models.Model):
    MOV_TYPES = [
        ('Entrada','Entrada'),
        ('Salida','Salida')
    ]
    product = models.ForeignKey(InventoryProduct, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    units = models.PositiveIntegerField()
    movType = models.CharField(max_length = 20, choices=MOV_TYPES)
