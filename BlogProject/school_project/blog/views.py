from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post

# Create your views here.
def home(request):
    context = { # this allows us to transfer data into the template under key 'posts'
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' # <app>/<models>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted'] # shows post from newest to oldest

# -- CRUD Functionality below --
class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    # this allows us to submit a post with the current auth user
    def form_valid(self, form):
        # before submitting the form, take the instance and set the author = current auth user
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    # this allows us to submit a post with the current auth user
    def form_valid(self, form):
        # before submitting the form, take the instance and set the author = current auth user
        form.instance.author = self.request.user
        return super().form_valid(form)

    # verifies that the user updating a post belongs only to them
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/' # if delete is successful, send user to home screen

    # verifies that the user deleting a post belongs only to them
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
