# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('albums', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='thumbnail',
            field=models.ForeignKey(default=None, related_name='+', null=True, to='images.Image'),
        ),
        migrations.AddField(
            model_name='album',
            name='users_like',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='liked_albums'),
        ),
    ]
