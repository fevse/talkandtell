from django.shortcuts import render
from .models import Post
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

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


class TTLoginView(LoginView):
    template_name = 'blog/login.html'

@login_required
def profile(request):
    return render(request, 'blog/profile.html')

class TTLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'blog/logout.html'
