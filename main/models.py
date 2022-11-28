from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserAccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email address must be provided')

        if not password:
            raise ValueError('Password must be provided')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True

        return self._create_user(email, password, **extra_fields)

class Course(models.Model):
    title = models.CharField(max_length=200, null=True)
    content = models.CharField(max_length=5000, null=True)
    url = models.CharField(max_length=200, null=True)
    cluster = models.IntegerField(null=True)
    site_name = models.CharField(max_length=50, null=True)
class Vacancy(models.Model):
    title = models.CharField(max_length=200, null=True)
    content = models.CharField(max_length=10000, null=True)
    url = models.CharField(max_length=200, null=True)
    salary = models.CharField(max_length=200, null=True)
    cluster = models.IntegerField(null=True)

class User(AbstractBaseUser, PermissionsMixin):
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = UserAccountManager()

    email = models.EmailField('email', unique=True, blank=False, null=False)
    full_name = models.CharField('full name', blank=True, null=True, max_length=400)
    is_staff = models.BooleanField('staff status', default=False)
    is_active = models.BooleanField('active', default=True)

    def get_short_name(self):
        return self.email

    def get_full_name(self):
        return self.email

    def __unicode__(self):
        return self.email
