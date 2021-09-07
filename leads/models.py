from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
  pass


class UserProfile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.user.username


class Lead(models.Model):
  first_name = models.CharField(max_length=20)
  last_name = models.CharField(max_length=20)
  age = models.PositiveIntegerField(default=0)
  agent = models.ForeignKey("Agent", on_delete=models.CASCADE)

  def __str__(self):
    return f"{self.first_name} {self.last_name}"


class Agent(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  organization = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

  def __str__(self):
    return self.user.email
