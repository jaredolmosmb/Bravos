from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, AbstractUser, PermissionsMixin, UserManager, BaseUserManager
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils import timezone
import uuid, random
from django.contrib.auth.models import Group

from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

class Reader(models.Model):
    file = models.FileField(blank=True, null=True)
    file2 = models.FileField(blank=True, null=True)
    date_uploaded = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date_uploaded']
        verbose_name_plural = "Reader"

class Player(models.Model):
	name = models.CharField(max_length=1000)
	position = models.CharField(max_length=1000)
	games_played = models.PositiveIntegerField()
	minutes_played = models.FloatField()
	yellow_cards = models.PositiveIntegerField()

	def __str__(self):
		return self.name
		
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

"""class Usuario(AbstractUser):
	telefono = models.CharField(max_length=15,default="")
	rol = models.IntegerField(default=0)

	@property
	def usuario_id(self):
		return unicode(self.id)
	def __str__(self):
		return self.email"""