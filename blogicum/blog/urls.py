from django.urls import path
from .views import (category_posts, create_post, DeletePostView, EditPostView,
                    index, post_detail)


app_name = 'blog'

urlpatterns = [
    path('', index, name='index'),
    path('posts/<int:id>/', post_detail, name='post_detail'),
    path('category/<slug:category_slug>/', category_posts,
         name='category_posts'),
    path('post/create/', create_post, name='create_post'),
    path(
        'posts/<int:post_id>/edit/',
        EditPostView.as_view(),
        name='edit_post'
    ),
    path(
        'posts/<int:post_id>/delete/',
        DeletePostView.as_view(),
        name='delete_post'
    )
]
