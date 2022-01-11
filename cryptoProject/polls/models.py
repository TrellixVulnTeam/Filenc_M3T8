from django.contrib.auth.models import AbstractUser
from django.db import models



# Create your models here.
class MyUser(AbstractUser):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=500, blank=True)
    username = models.CharField(max_length=255, unique=True, blank=True)
    password = models.CharField(max_length=255, blank=True)
    key = models.CharField(max_length=255, blank=True)
    iv = models.CharField(max_length=255, blank=True)
    #
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []


class Files(models.Model):
    file = models.FileField(upload_to="static/files")
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)


def __str__(self):
    return self.username
