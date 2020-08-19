from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from django import forms
# Create your models here.
SUBJECT = (
    (1, 'English'),
    (2, 'Programming'),
    (3, 'Mathematics'),
    (4, 'Others')
)


class StudyModel(models.Model):
    date = models.DateTimeField(default=timezone.now,null=True)
    author = models.CharField(max_length=100)
    subject = models.IntegerField(verbose_name='科目', choices=SUBJECT, default=None)
    content = models.TextField(default=None, null=True)
    study_time = models.FloatField(blank=True, null=True, default=0)
    images = models.ImageField(upload_to='',blank=True)
