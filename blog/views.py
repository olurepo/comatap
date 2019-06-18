from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .models import Post, Category, Comment
from .forms import CommentForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


def home(request):
    
    context = {
        'posts': Post.objects.all(),
    }

    return render(request, 'blog/home.html', context)

def about(request):

    return render(request, 'blog/about.html', {'title': 'About'})


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 3

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    #ordering = ['-date_posted']  # order_by('-date_posted') in the query overrides this
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username')) # see how this can be useful to get 'proj_name'
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):   # function uses post_detail.html
    model = Post
    context_object_name = 'posts'

# ==== COULDN'T FIGURE OUT HOW Class-based View works for forms yet =====#

def post_category(request, category):
    posts = Post.objects.filter(categories__name__contains=category).order_by('-date_posted')
    context = {
        'category': category,
        'posts': posts
    }
    return render(request, 'blog/post_category.html', context)

def post_detail(request, pk):
    post = Post.objects.get(pk=pk)

    #this form handles readers comments
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            comment = Comment(
                author = form.cleaned_data["author"],
                content = form.cleaned_data["content"],
                post = post,
            )
            comment.save()

    comments = Comment.objects.filter(post=post)

    context = {
        'post': post,
        'comments': comments,
        'form': form,
    }
    
    return render(request, 'blog/details.html', context)

# ==== COULDN'T FIGURE OUT HOW Class-based View works for forms yet =====#


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'categories']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
#=============  POST  END  ================#