from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.PostListView.as_view(), name='posts'),
    path('post/<int:pk>', views.PostDetailView.as_view(), name='post_detail'),
    path('post/create/', views.PostCreate.as_view(), name='post-create'),
    path('post/<int:pk>/update/', views.PostUpdate.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.PostDelete.as_view(), name='post-delete'),
    path('accounts/login/', views.TTLoginView.as_view(), name='login'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/logout/', views.TTLogoutView.as_view(), name='logout'),

]