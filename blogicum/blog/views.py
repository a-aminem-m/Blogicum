from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import DeleteView, UpdateView

from .forms import CommentForm, EditCommentForm, EditProfileForm, PostForm
from .models import Category, Comment, Post

from . import constants


def get_paginated_posts(post_list, posts_limit):
    paginator = Paginator(post_list, posts_limit)
    return paginator


def get_base_post_queryset():
    return Post.objects.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True,
    ).select_related(
        'author',
        'location',
        'category'
    ).annotate(
        comment_count=Count('comments')
    ).order_by('-pub_date')


def index(request):
    post_list = get_base_post_queryset()
    page_number = request.GET.get('page')
    page_obj = get_paginated_posts(
        post_list, constants.POSTS_LIMIT
    ).get_page(page_number)
    return render(request, 'blog/index.html', {'page_obj': page_obj})


def post_detail(request, post_id):
    post = get_object_or_404(Post.objects.select_related(
        'author', 'location', 'category'), id=post_id)
    if request.user != post.author:
        post = get_object_or_404(get_base_post_queryset(), id=post_id)
    comments = post.comments.all()
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
    context = {'user': request.user,
               'post': post,
               'comments': comments,
               'form': form}
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    posts = get_base_post_queryset().filter(category=category)
    page_number = request.GET.get('page')
    page_obj = get_paginated_posts(
        posts,
        constants.POSTS_LIMIT
    ).get_page(page_number)
    context = {'category': category, 'page_obj': page_obj}
    return render(request, 'blog/category.html', context)


@login_required
def create_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect(
            'blog:profile',
            request.user.username,
        )
    return render(request, 'blog/create.html', {'form': form})


class EditPostView(UpdateView):
    model = Post
    pk_url_kwarg = 'post_id'
    form_class = PostForm
    template_name = 'blog/create.html'

    def get_success_url(self):
        return reverse('blog:post_detail', args=(self.kwargs['post_id'],))

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            return redirect('blog:post_detail', self.kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)


class DeletePostView(DeleteView):
    model = Post
    pk_url_kwarg = 'post_id'
    form_class = PostForm
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        if request.user == self.object.author or request.user.is_staff:
            success_url = self.get_success_url()
            self.object.delete()
            return redirect(success_url)
        return self.render_to_response(self.get_context_data())


def profile(request, username):
    user_profile = get_object_or_404(User, username=username)
    if user_profile != request.user:
        post_list = get_base_post_queryset().filter(author__username=username)
    else:
        post_list = user_profile.posts.all().select_related(
            'author', 'location', 'category'
        ).annotate(
            comment_count=Count('comments')).order_by('-pub_date')
    paginator = Paginator(post_list, constants.POSTS_LIMIT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'profile': user_profile,
        'page_obj': page_obj,
        'user': request.user,
    }
    return render(request, 'blog/profile.html', context)


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'blog/user.html'

    def get_success_url(self):
        return reverse('blog:profile',
                       kwargs={'username': self.request.user.username})

    def get_object(self, queryset=None):
        return self.request.user

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj != self.request.user:
            return redirect(
                'blog:profile',
                username=self.request.user.username
            )
        return super().dispatch(request, *args, **kwargs)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(
        get_base_post_queryset(),
        id=post_id,
    )
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        return redirect('blog:post_detail', post_id=post_id)
    return render(request, 'blog/comment.html', {'form': form, 'post': post})


def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.author:
        return redirect(comment.post.get_absolute_url())
    form = EditCommentForm(instance=comment)
    if request.method == 'POST':
        form = EditCommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect(comment.post.get_absolute_url())
    context = {'comment': comment, 'form': form}
    return render(request, 'blog/comment.html', context)


class DeleteCommentView(DeleteView):
    model = Comment
    pk_url_kwarg = 'comment_id'
    form_class = CommentForm
    template_name = 'blog/comment.html'
    success_url = reverse_lazy('blog:profile')

    def get_success_url(self):
        post_id = self.kwargs.get('post_id')
        return reverse('blog:post_detail', kwargs={'post_id': post_id})

    def dispatch(self, request, *args, **kwargs):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)

        comment = get_object_or_404(
            Comment,
            id=self.kwargs['comment_id'],
            post=post,
            post__is_published=True
        )

        if comment.author != self.request.user:
            return redirect(comment.post.get_absolute_url())

        return super().dispatch(request, *args, **kwargs)
