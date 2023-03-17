from django.db import models
from django import forms
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
import uuid
from django.shortcuts import render

# Create your models here.

class TTUser(AbstractUser):
    is_activated = models.BooleanField(
        default=True, db_index=True, verbose_name='Активация пройдена?'
        )
    
    send_message = models.BooleanField(
        default=True, verbose_name='Оповещать о новых постах?'
        )
    
    def __str__(self) -> str:
        return self.username

    def get_absolute_url(self):
        return reverse('user_detail', args=[str(self.id)])


    class Meta(AbstractUser.Meta):
        pass


class Post(models.Model):
    
    author = models.ForeignKey(TTUser, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=128, verbose_name='Заголовок')
    body = models.TextField(max_length=1024, verbose_name='Основной текст')
    post_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    class Meta:
    	ordering = ["-post_date"]


class Comment(models.Model):
    
    author = models.ForeignKey(TTUser, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    body = models.TextField(max_length=255, verbose_name='Комментарий')
    comment_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return self.body
    
    def get_absolute_url(self):
        return reverse('comment', args=[str(self.id)])
    
    class Meta:
        ordering = ["-comment_date"]





