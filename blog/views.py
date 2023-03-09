from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Post, TTUser
from .forms import PostForm

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

@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            messages.add_message(request, messages.SUCCESS, 'Пост добавлен')
    else:
        form = PostForm(initial={'author': request.user.pk})
    context = {'form': form}
    return render(request, 'blog/post_create.html', context=context)




''' удалить после проверки функции добавления нового поста
class PostCreate(generic.CreateView):
    model = Post
    fields = ['title', 'body']
    initial = {'author': TTUser.username}
'''


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
