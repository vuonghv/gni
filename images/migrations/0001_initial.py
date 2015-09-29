# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import images.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('albums', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('img', models.ImageField(upload_to=images.models._path_to_file, width_field='width', max_length=257, height_field='height')),
                ('width', models.PositiveSmallIntegerField(default=650)),
                ('height', models.PositiveSmallIntegerField(default=750)),
                ('title', models.TextField(default='', blank=True)),
                ('description', models.TextField(default='', blank=True)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('time_updated', models.DateTimeField(auto_now=True)),
                ('album', models.ForeignKey(related_name='images', null=True, to='albums.Album')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='images')),
                ('users_like', models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='liked_images')),
            ],
        ),
    ]
