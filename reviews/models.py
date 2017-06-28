from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator


class Review(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    product = models.ForeignKey('product.Product')
    rating = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ]
    )
