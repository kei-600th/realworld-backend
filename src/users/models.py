from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
  def create_user(self, username, email, password=None):
    if username is None:
        raise TypeError('Users must have a username.')

    if email is None:
        raise TypeError('Users must have an email address.')

    email = self.normalize_email(email)

    user = self.model(username=username, email=email)
    user.set_password(password)
    user.save()

    return user


class User(AbstractUser):
  objects = UserManager()
