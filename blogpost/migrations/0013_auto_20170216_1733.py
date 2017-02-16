# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-16 17:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogpost', '0012_auto_20170214_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user_group',
            field=models.CharField(choices=[('FL', 'Follower'), ('WR', 'Writer')], default='FL', max_length=2),
        ),
    ]
