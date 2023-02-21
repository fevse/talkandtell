from django.shortcuts import render
from .models import Post
from django.views import generic
from django.urls import reverse, reverse_lazy

# Create your views here.
def index(request):
    num_posts = Post.objects.all().count()
    num_visits = request.session.get('num_visits', 0)

    request.session['num_visits'] = num_visits+1

    return render(
        request,
        'index.html',
        context=
        {'num_posts': num_posts,
        'num_visits': num_visits},
    )


class PostListView(generic.ListView):
    model = Post
    paginate_by = 10

class PostDetailView(generic.DetailView):
    model = Post

class PostCreate(generic.CreateView):
    model = Post
    fields = ['title', 'body']

class PostUpdate(generic.UpdateView):
    model = Post
    fields = ['title', 'body']

class PostDelete(generic.DeleteView):
    model = Post
    success_url = reverse_lazy('posts')
