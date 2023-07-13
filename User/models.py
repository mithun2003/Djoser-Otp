from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from datetime import timedelta
from django.utils.timezone import make_aware


class MyAccountManager(BaseUserManager):
    def create_user(self,name,email,password=None,**kwargs):
        if not email:
            raise ValueError("User must have an email")
        
        email = self.normalize_email(email)
        user = self.model(email=email,name=name,**kwargs)
        
        user.set_password(password)
        user.save()
        
        return user
    def create_superuser(self ,name, email, password,**kwargs):
        user = self.create_user(
            email = email,
            name  = name,
            password = password,
            **kwargs
        )

        user.is_admin = True
        user.is_staff = True 
        user.is_active = True
        user.is_verified = True
        user.is_superuser = True
        user.save(using=self._db)
        return 
    

class UserAccount(AbstractBaseUser):
    name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(max_length=100, unique=True, blank=False)
    mobile_number = models.CharField(max_length=20,blank=True, null=True)
    country = models.CharField(max_length=50,blank=True, null=True)
    image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','image']

    objects = MyAccountManager()

    def __str__(self):
        return f"{self.name} - {self.email}"


    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
