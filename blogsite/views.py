from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from django.contrib.auth.models import User


# Create your views here.
def index(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blogsite/index.html', context)


class PostListView(ListView):
    # what model to query when creating the list
    model = Post
    template_name = 'blogsite/index.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'  # same name as in the index view and in index.html
    # changes the ordering to reverse chronological
    ordering = ['-date_posted']
    paginate_by = 10


class UserPostListView(ListView):
    # what model to query when creating the list
    model = Post
    template_name = 'blogsite/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'  # same name as in the index view and in index.html
    paginate_by = 10

    def get_queryset(self):
        # gets the username from the URL
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    # set the author of the post as the user making the request
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)  # runs the form_valid method on the parent class


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    # set the author of the post as the user making the request
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)  # runs the form_valid method on the parent class

    # checks that the user is the author of the post and if so, allow them to update the post
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    # checks that the user is the author of the post and if so, allow them to delete the post
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blogsite/about.html', {'title': 'About'})
