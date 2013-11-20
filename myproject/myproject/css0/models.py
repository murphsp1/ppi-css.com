# -*- coding: utf-8 -*-
from django.db import models
from django.utils.timezone import utc
import datetime

class Document(models.Model):
    docfile = models.FileField(upload_to='documents/')


class Scores(models.Model):
	name = models.CharField(max_length=30)
	score = models.FloatField()
	interface = models.CharField(max_length=30)
	uploaded = models.BooleanField(default=False) 
	#date_uploaded = models.DateTimeField(default=datetime.datetime.now())
	date_uploaded = models.DateTimeField(default = datetime.datetime.utcnow().replace(tzinfo=utc))
