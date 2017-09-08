# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from jsonfield import JSONField


class Location(models.Model):
    place = models.CharField(max_length=20)
    population = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class SaveLocation(models.Model):
    json = JSONField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
