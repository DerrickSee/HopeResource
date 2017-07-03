# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-03 08:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('churches', '0004_auto_20170628_0628'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='churchmembership',
            name='is_owner',
        ),
        migrations.RemoveField(
            model_name='churchmembership',
            name='is_staff',
        ),
        migrations.AddField(
            model_name='churchmembership',
            name='permission',
            field=models.IntegerField(choices=[(1, 'Owner'), (2, 'Staff'), (3, 'Member')], default=3),
        ),
    ]