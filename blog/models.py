from django.db import models
from django import forms
from django.urls import reverse
from django.contrib.auth.models import User
import uuid
from datetime import date
from django.shortcuts import render

# Create your models here.


class Post(models.Model):
    # author = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200, help_text='title of your post')
    body = models.TextField(max_length=1000, help_text='your post')


    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

