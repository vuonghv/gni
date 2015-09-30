# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('content', models.TextField()),
                ('time_updated', models.DateTimeField(auto_now=True)),
                ('image', models.ForeignKey(to='images.Image', related_name='comments')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='comments')),
                ('users_like', models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='liked_comments')),
            ],
        ),
    ]
