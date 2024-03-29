from __future__ import unicode_literals

from django.db import models
from django.conf import settings

from saleor.userprofile.models import Address


class Church(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50)
    address = models.ForeignKey(Address, null=True, on_delete=models.SET_NULL)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through='ChurchMembership')
    blacklist = models.ManyToManyField("product.Product")

    def __str__(self):
        return self.name


class ChurchMembership(models.Model):
    church = models.ForeignKey(Church, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_joined = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=250, default="Member")
    permission = models.IntegerField(choices=[
        (1, 'Owner'),
        (2, 'Staff'),
        (3, 'Member'),
    ], default=3)

    class meta:
        ordering = ("permission", "title")
