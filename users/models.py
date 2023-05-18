from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError("You must provide an email.")
        if not password:
            raise ValueError("You must set a password.")
        
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        
        return self.create_user(email, password, **extra_fields)


class CustomUserModel(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class UserProfileModel(models.Model):
    user = models.ForeignKey('CustomUserModel', null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    gender = models.CharField(max_length=200, null=True)
    phone_number = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.first_name


class UserVideoModel(models.Model):
    user = models.ForeignKey('CustomUserModel', null=True, on_delete=models.CASCADE)
    video_title = models.CharField(max_length=200, null=True)
    video_duration = models.CharField(max_length=200, null=True)
    video_image = models.CharField(max_length=200, null=True)
    video_text = models.CharField(max_length=200, null=True)
    video_effect = models.CharField(max_length=200, null=True)
    data_created = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return self.video_title






