from django.views.generic import RedirectView
from django.urls import path, reverse_lazy
from .views import (add_comment, category_posts, create_post,
                    DeleteCommentView, DeletePostView, edit_comment,
                    EditPostView, EditProfileUpdateView, index, post_detail,
                    profile)


app_name = 'blog'

urlpatterns = [
    path('', index, name='index'),
    path('posts/create/', create_post, name='create_post'),
    path('posts/<int:post_id>/', post_detail, name='post_detail'),
    path('category/<slug:category_slug>/', category_posts,
         name='category_posts'),
    path('posts/<int:post_id>/edit/',
         EditPostView.as_view(),
         name='edit_post'),
    path('posts/<int:post_id>/delete/',
         DeletePostView.as_view(),
         name='delete_post'),
    path('posts/<post_id>/comment/', add_comment, name='add_comment'),
    path('posts/<post_id>/edit_comment/<comment_id>/',
         edit_comment,
         name='edit_comment'),
    path('posts/<post_id>/delete_comment/<comment_id>/',
         DeleteCommentView.as_view(),
         name='delete_comment'),
    path('profile/password/',
         RedirectView.as_view(url=reverse_lazy('password_change')),
         name='custom_password_change'),
    path('profile/edit_profile/',
         EditProfileUpdateView.as_view(),
         name='edit_profile'),
    path('profile/<username>/', profile, name='profile'),

]
