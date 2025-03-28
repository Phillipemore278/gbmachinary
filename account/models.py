from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _
from django.db import models
from .managers import CustomAccountManager


class Customer(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    full_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    country = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    
    

    objects = CustomAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"
        ordering = ('-created',)
        

    def __str__(self):
        return self.full_name+ ', ' + self.email
    

class MyClient(models.Model):
    c_email = models.EmailField()
    c_full_name = models.CharField(max_length=255)
    c_country = models.CharField(max_length=100, null=True, blank=True)
    c_city = models.CharField(max_length=100, null=True, blank=True)
    c_address = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "My Client"
        verbose_name_plural = "My Clients"
        ordering = ('-created',)
        

    def __str__(self):
        return self.full_name

