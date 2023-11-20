from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import DeleteView, UpdateView
from .forms import PostForm
from .models import Category, Post


POSTS_LIMIT = 10


def get_base_post_queryset():
    current_time = timezone.now()
    base_queryset = Post.objects.filter(
        pub_date__lte=current_time,
        is_published=True,
        category__is_published=True,
    ).select_related('author', 'location', 'category')
    return base_queryset


def index(request):
    post_list = get_base_post_queryset()
    paginator = Paginator(post_list, POSTS_LIMIT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/index.html', {'page_obj': page_obj})


def post_detail(request, id):
    post = get_object_or_404(get_base_post_queryset(), id=id)
    context = {'post': post}
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(Category.objects.filter(is_published=True),
                                 slug=category_slug)
    posts = get_base_post_queryset().filter(
        category=category).order_by('-pub_date')
    context = {'category': category, 'post_list': posts}
    return render(request, 'blog/category.html', context)


def create_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('blog:index')
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
