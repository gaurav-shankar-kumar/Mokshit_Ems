from datetime import datetime
from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager ## A new class is imported. ##
from django.utils.translation import gettext_lazy as _
from birthday import BirthdayField, BirthdayManager

from django.conf import settings



# Create your models here.

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User_Group(models.Model):
    group_name = models.CharField(max_length=50,unique=True)
    def __str__(self):
        return self.group_name

class Tech(models.Model):
    tech_name = models.CharField(max_length=100,blank=True,null=True,unique=True)
    def __str__(self):
        return self.tech_name

Gender_Choices = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)

Role_choise =(
    ("Project Manager", "Project Manager"),
    ("Team Leader", "Team Leader"),
    ("Manager", "Manager"),
    ("Developer", "Developer"),
    ("HR", "HR"),
    ("Junior Developer", "Junior Developer"),
    ("Trainee", "Trainee"),
)

Emptype_choise = (
    ("Full-Time","Full-Time"),
    ("Part-Time","Part-Time"),
    ("Contract","Contract"),
    ("Intern","Intern"),
    )


class User(AbstractUser):
    username = None
    USERNAME_FIELD = 'email'
    email = models.EmailField(unique=True)
    dob =  BirthdayField(blank=True, null=False)
    group = models.ForeignKey(User_Group,blank=True, null=True, on_delete=models.SET_NULL)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    designation = models.CharField(max_length=20, null=False,blank=True)
    position = models.CharField(max_length=50,default='test')
    joining_date = models.DateTimeField(null=True)
    emp_type = models.CharField(choices=Emptype_choise, max_length=60,default='test',null=True)
    role = models.CharField(choices=Role_choise, max_length=60,default='test',null=True)
    is_hr = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    gender = models.CharField(max_length = 20,choices = Gender_Choices,blank=True, null=True)
    blood_group = models.CharField(max_length=10, blank=True)
    address = models.CharField(max_length=500, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    avatar = models.ImageField(upload_to=f'user_avatars/', blank=True, null=True,default='user_avatars/default.jpg')
    tech = models.ManyToManyField(Tech)
    REQUIRED_FIELDS = []
    objects = UserManager()
    empbday = BirthdayManager()


class Bank_Details(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='bank_details')
    bank_name = models.CharField(max_length=100)
    ac_no = models.CharField(max_length=100)
    ifsc_no = models.CharField(max_length=100)
    pf_no = models.CharField(max_length=100,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    action_by = models.ForeignKey(User,related_name = 'bank_details_by',on_delete=models.SET_NULL,blank=True,null=True)





    
    
    




