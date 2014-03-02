from django.db import models
from django.contrib.auth.models import User

from shoppingcart.fields import CurrencyField

class Store(models.Model):
    name = models.CharField(max_length=200, unique=True)
    sub_domain = models.CharField(max_length=200, unique=True)
    custom_css = models.URLField(blank=True)
    custom_body = models.URLField(blank=True)

    def __unicode__(self):
        return u'%s' % (self.name)


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    store = models.ForeignKey(Store)

    def __str__(self):
          return "%s's profile" % self.user

class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    img_url = models.URLField(default="http://lorempixel.com/250/250/")
    thumbnail_url = models.URLField(default="http://lorempixel.com/50/50")
    price = CurrencyField(default=0, decimal_places=2, max_digits=10)
    inventory = models.IntegerField(default=0)
    store = models.ForeignKey(Store)

    def __unicode__(self):
        return u'%s' % (self.name)
