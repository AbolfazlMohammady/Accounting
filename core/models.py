import re
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser, BaseUserManager

def  validate_phone_number(value):
    if not re.match(r'^09\d{9}$',value):
        return ValidationError("شماره تلفن باید با 09 شروع شود و 11 رقم باشد.")



class CustomUserManager(BaseUserManager):
    def create_user(self, phone=None, email=None, password=None, **extra_fields):
        if not phone and not email:
            raise ValueError('شماره تلفن یا ایمیل باید تنظیم شود.')

        user = self.model(phone=phone, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('سوپرکاربر باید is_staff=True داشته باشد.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('سوپرکاربر باید is_superuser=True داشته باشد.')
        return self.create_user(phone, email, password, **extra_fields)


class User(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'کاربر عادی'),
        ('admin', 'ادمین'),
        ('finance', 'مدیر مالی'),
    ]
    first_name = None
    last_name = None
    username= None
    full_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=11,
                            blank=True, 
                            unique=True,
                            null=True,
                            default='unknown',
                            validators=[validate_phone_number],
                            help_text='لطفا شماره تلفن خود را  وارد کنید')
    email = models.EmailField(blank=True, null=True)
    image = models.ImageField(upload_to='profile',blank=True, null=True)
    bio =models.CharField(max_length=1011,blank=True, null=True )
    age = models.DateField(blank=True,null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    gender = models.CharField(max_length=11, choices=[('male','مردی'), ('female','زن')],blank=True, null=True)

    objects = CustomUserManager()
    
    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["email"]


    # متدهای دسترسی به نقش‌ها
    def is_admin(self):
        return self.role == 'admin'

    def is_finance_manager(self):
        return self.role == 'finance'

    def is_user(self):
        return self.role == 'user'

    def __str__(self):
        return self.email or self.phone or "کاربر بدون نام"
