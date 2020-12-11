from django.db import models
from django.urls import reverse
import unique_key
from django.db import IntegrityError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# User Manager

class MyUserManager(BaseUserManager):

    # UNIQUE WILL BE HERE

    def create_user(self, first_name, last_name, email, gender, password=None):
        """
        Creates and saves a User with the given information.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not first_name:
            raise ValueError('Users must have first name')
        if not last_name:
            raise ValueError('Users must have last name')
        # if not username:
        #     raise ValueError('Users must have a username')
        # if not phone_number:
        #     raise ValueError('Users must have an email address valid phone number')
        if not gender:
            raise ValueError('Users must specify gender')
        # if not country:
        #     raise ValueError('Users must have a country')

        user = self.model(
            email=self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            # username = username,
            # phone_number = phone_number,
            gender = gender,

            unique_id = unique_key.gen_unique_key()
            # country = country
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, gender, password=None):
        """
        Creates and saves a superuser with the given information.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            # username = username,
            # phone_number = phone_number,
            gender = gender,
            # country = country,

            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.email_confirmed = True
        user.save(using=self._db)
        return user

# Create your models here.
class User(AbstractBaseUser):

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Others')
    )

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True, max_length=254)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    # phone_number = models.CharField(null=True, blank=True, unique=True, max_length=15)
    # country = models.CharField(max_length = 20, null=True, blank=True)
    # referrer = models.CharField(max_length = 20, null=True, blank=True)
    unique_id = models.CharField(unique = True, max_length = 50, null=True, blank=True)
    email_confirmed = models.BooleanField(default = False)
    registered_on = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'gender']
    USERNAME_FIELD = 'email'

    object = MyUserManager()

    def __str__(self):
        return self.first_name+" "+self.last_name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def get_absolute_url(self):
        return reverse("account:account", kwargs={'unique_id': self.unique_id})
