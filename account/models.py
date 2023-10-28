from typing import Iterable, Optional
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager,AbstractUser
from django.contrib.auth.hashers import make_password
from django.contrib import auth
import uuid
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.apps import apps


# Create your models here.

class CustomUserManager(BaseUserManager):
    use_in_migrations = True
    def _create_user(self,email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        email = GlobalUserModel.normalize_username(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    
class CustomUser(AbstractBaseUser,PermissionsMixin):
    id=models.UUIDField(primary_key=True,editable=False,db_index=True,default=uuid.uuid4)
    first_name=models.CharField(_("First_name"),max_length=400)
    last_name=models.CharField(_("Last_name"),max_length=400)
    email=models.EmailField(_("Email Address"),unique=True,)
    phone_no=models.CharField(_("Phone Number"),unique=True,max_length=12,blank=True,null=True)
    is_staff = models.BooleanField(_("staff status"), default=False )
    is_active = models.BooleanField( _("active"),default=True,)
    is_verified = models.BooleanField( _("Verified"),default=False,)
    is_instrutor=models.BooleanField(_("Instructor"),default=False)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    confirm_password=models.CharField(max_length=100)

    EMAIL_FIELD = ""
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects=CustomUserManager()


    def __str__(self) -> str:
        return self.get_full_name()
    
    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def save(self,**kwargs):
        self.first_name= self.first_name.title()
        self.last_name= self.last_name.title()
        if self.is_superuser:
            self.is_verified=True
            self.is_instrutor=True
        return super().save(**kwargs)

    

class PhoneNumberVerification(models.Model):
    id=models.UUIDField(primary_key=True,editable=False,db_index=True,default=uuid.uuid4)
    phone_no=models.CharField(_("Phone Number"),unique=False,max_length=12,blank=True,null=True)
    otp_code=models.CharField(max_length=6,unique=False,blank=True,null=True)
    # verify=models.BooleanField(default=False)
    date_generated=models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return self.phone_no