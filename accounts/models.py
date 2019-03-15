from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as lazy

BOOL_CHOICES = [(True, 'Yes'), (False, 'No')]


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


class VanLevyUser(AbstractUser):
    username = models.CharField(max_length=100,  unique=True)
    email = models.EmailField(lazy('email address'), unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']


class UserProfile(models.Model):
    user = models.OneToOneField(VanLevyUser, on_delete=models.CASCADE)
    user_bio = models.CharField(max_length=500, default='', blank=True)
    user_description = models.CharField(max_length=500, default='', blank=True)
    user_image = models.ImageField(upload_to='profile_image', blank=True)
    user_url_image = models.URLField(max_length=500, blank=True, default='')
    user_first_name = models.CharField(max_length=100, default='', blank=True)
    user_last_name = models.CharField(max_length=100, default='', blank=True)
    user_location = models.CharField(max_length=300, default='', blank=True)

    def __str__(self):
        return self.user.username


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=VanLevyUser)


class Avatar(models.Model):
    user = models.ForeignKey(VanLevyUser, on_delete=models.CASCADE)
    avatar_name = models.CharField(max_length=200, default='', blank=True)
    avatar_description = models.CharField(max_length=500, default='', blank=True)
    avatar_image = models.ImageField(upload_to='avatar_image', blank=True)
    avatar_url_image = models.URLField(max_length=300, blank=True, default='')
    created_on = models.DateTimeField(blank=True, null=True)
    deleted = models.BooleanField(choices=BOOL_CHOICES, default=False)

    def __str__(self):
        if self.avatar_name == '':
            return self.user.username
        else:
            return self.avatar_name
