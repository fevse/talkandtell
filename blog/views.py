from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.db.models import Q 
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.signing import BadSignature

from .models import Post, TTUser, Comment
from .forms import PostForm, CommentForm, ChangeUserInfoForm, RegisterUserForm
from .utilites import signer

# Create your views here.
def index(request):
    num_posts = Post.objects.all().count()
    num_users = TTUser.objects.all().count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    context = {
    	'num_posts': num_posts,
        'num_users': num_users,
        'num_visits': num_visits
        }

    return render(
        request,
        'index.html',
        context=context,
    )


class PostListView(generic.ListView):
    model = Post
    paginate_by = 10

class PostDetailView(generic.DetailView):
    model = Post
    paginate_by = 5

@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            messages.add_message(request, messages.SUCCESS, 'Пост добавлен')
            return HttpResponseRedirect(reverse('posts'))
    else:
        form = PostForm(initial={'author': request.user.pk})
    context = {'form': form}
    return render(request, 'blog/post_create.html', context=context)

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


class ChangeUserInfoView(generic.UpdateView, LoginRequiredMixin):
    model = TTUser
    template_name = 'blog/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('profile')

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)
    
    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)

class TTPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'blog/password_change.html'
    success_url = reverse_lazy('profile')


class RegisterUserView(generic.CreateView):
    model = TTUser
    template_name = 'blog/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('register_done')

class RegisterDoneView(generic.TemplateView):
    template_name = 'blog/register_done.html'


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'blog/bad_signature.html')
    user = get_object_or_404(TTUser, username=username)
    if user.is_activated:
        template = 'blog/user_is_activated.html'
    else:
        template = 'blog/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)

@login_required
def comment_create(request, pk):
    note = Post.objects.get(pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save()
            messages.add_message(request, messages.SUCCESS, 'Коментарий добавлен')
            return HttpResponseRedirect(reverse_lazy('post_detail', kwargs={'pk': pk}))
    else:
        qqq = request
        form = CommentForm(initial={'author': qqq.user.pk, 'post': note})
    context = {'form': form}
    return render(request, 'blog/comment_create.html', context=context)

class SearchResultsView(generic.ListView):
    model = Post
    template_name = 'search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Post.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query) | Q(author__username__icontains=query)
        )
        return object_list
