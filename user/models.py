from datetime import datetime 
from django.db import models
from common.models import BaseModel
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.postgres.fields import ArrayField

from django.db import models

DAY_MAPPING = {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday',
    5: 'Saturday',
    6: 'Sunday',
}

class Pathology(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    image = models.ImageField(upload_to='pathology_images/', blank=True, null=True)
    fcm_token = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    is_offline = models.BooleanField(default=False)
    working_days = ArrayField(models.IntegerField(), size=7,null=False,default=[0,1,2,3,4,5,6])
    not_working_dates = ArrayField(models.DateTimeField(auto_now_add=True),null=True)
    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):
    def create_user(self, google_id=None, password=None, **extra_fields):
        if not google_id: 
            raise ValueError("The google id field must be set")
        user = self.model(google_id=google_id, **extra_fields)
        user.google_id = google_id
        user.username = google_id
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,google_id=None, password=None, **extra_fields):
        return self.create_user( google_id,password, **extra_fields)
    
class User(AbstractUser):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, default='')
    is_phone_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    profile_pic = models.ImageField(
        upload_to='profile_pics/', blank=True, null=True)
    email = models.EmailField(unique=False)
    invited_by = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL)
    google_id = models.CharField(blank=False, null=False, unique = True)
    
    
    USERNAME_FIELD = 'google_id'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    
    class Meta:
        ordering = 'id',

class Notification(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    type_id = models.CharField(max_length=255)
    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL)

class Patient(BaseModel):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=15, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    
    def __str__(self):
        return self.name

class Address(BaseModel):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}, {self.postal_code}"