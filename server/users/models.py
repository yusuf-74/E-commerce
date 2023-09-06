from django.db import models
from django.contrib.auth.models import AbstractUser

ROLES = (
    ("customer", "Customer"),
    ("seller", "Seller"),
    ("staff", "Staff"),
)

class User(AbstractUser):

    role = models.CharField(max_length=50,choices=ROLES, default="customer")
    country_code = models.CharField(max_length=10, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.username


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    flat = models.CharField(max_length=15)
    block = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    state = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=15,blank=True, null=True)
    country = models.CharField(max_length=20)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.pk
