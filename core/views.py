from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, DeleteView, CreateView

from .forms import CommentForm, PostForm, RegistrationForm
from .models import Post, Comment


class IndexView(TemplateView):
    def get(self, request, **kwargs):
        content = {}
        return render(request, 'core/index.html', content)


class PostListView(ListView):
    queryset = Post.objects.all()


class MyPostListView(TemplateView):
    def get(self, request, *args, **kwargs):
        user = request.user
        post_list = user.post_set.all()
        context = {'post_list': post_list,
                   'my_posts': True}
        return render(request, 'core/post_list.html', context)


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['is_author'] = (context['post'].author == self.request.user)
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ('title', 'content')

    def form_valid(self, form):
        form = form.save(commit=False)
        form.author = self.request.user
        form.save()
        return redirect(form.get_absolute_url())


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('my-post-list')

    def delete(self, request, *args, **kwargs):
        if request.user.id != Post.objects.get(pk=kwargs['pk']).author.id:
            raise PermissionDenied
        return super(PostDeleteView, self).delete(request, *args, *kwargs)


class CommentPostView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        author = User.objects.get(username=request.POST['author'])
        form = CommentForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = author
            form.post = post
            form.save()
        return redirect(post.get_absolute_url())

    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        return redirect(post.get_absolute_url())


class CommentDeleteView(View):
    def post(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        success_url = comment.post.get_absolute_url()
        if request.user == comment.author:
            comment.delete()
        else:
            raise PermissionDenied
        return redirect(success_url)


class RegistrationView(View):
    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(reverse('index'))
        return render(request, 'registration/signup.html', {'form': form})


    def get(self, request):
        form = UserCreationForm()
        return render(request, 'registration/signup.html', {'form': form})

