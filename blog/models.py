from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200, help_text='title of your post')
    body = models.TextField(max_length=1000, help_text='your post')


    def __str__(self) -> str:
        return self.title