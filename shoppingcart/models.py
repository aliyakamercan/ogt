from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Store(models.Model):
    name = models.CharField(max_length=200, unique=True)
    sub_domain = models.CharField(max_length=200, unique=True)
    custom_css = models.URLField(blank=True)
    custom_body = models.URLField(blank=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    store = models.ForeignKey(Store)

    def __str__(self):
          return "%s's profile" % self.user
