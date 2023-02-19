from django.shortcuts import render
from .models import Post
from django.views import generic

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
