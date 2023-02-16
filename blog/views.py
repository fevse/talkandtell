from django.shortcuts import render
from .models import Post
from django.views import generic

# Create your views here.


class PostListView(generic.ListView):
    model = Post
    context_object_name = 'post_list'

