from __future__ import unicode_literals

from django.db import models

from saleor.userprofile.models import Address

# Create your models here.
class Church(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50)
    address = models.ForeignKey(Address)

    def __str__(self):
        return self.name
