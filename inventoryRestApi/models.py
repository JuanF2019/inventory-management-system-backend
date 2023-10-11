from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

class Brand(models.Model):
    name = models.CharField(max_length=100)

class Permission(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

class Role(models.Model):
    name = models.CharField(max_length=100)
    permissions = models.ManyToManyField(Permission)

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

class User(models.Model):
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
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    document = models.CharField(max_length=10)
    docType = models.CharField(max_length=4, choices=DOCUMENT_TYPES)
    email = models.CharField(max_length=100)
    phoneNumber = models.CharField(max_length=15)
    birthday = models.DateField()
    role = models.ForeignKey(Role, on_delete=models.PROTECT)

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
