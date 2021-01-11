from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):

    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    profile_pic = models.ImageField(default="default.png", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Tag(models.Model):

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):

    CATEGORY = (
        ('Indoor', 'Indoor'),
        ('Outdoor', 'Outdoor')
    )

    name = models.CharField(max_length=255)
    price = models.DecimalField(decimal_places=2, max_digits=15)
    category = models.CharField(max_length=255, choices=CATEGORY)
    description = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)


    def __str__(self):
        return self.name


class Order(models.Model):

    STATUS = (
        ('Pending', 'Pending'),
        ('Out of delivery', 'Out of delivery'),
        ('Delivered', 'Delivered')
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, choices=STATUS)
    note = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"{self.customer.name} - {self.status}"
