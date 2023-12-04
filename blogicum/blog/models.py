from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from . import constants


class StatusModel(models.Model):
    is_published = models.BooleanField(
        default=True,
        verbose_name='Published',
        help_text='Uncheck the box to hide the post.'
    )
    created_at = models.DateTimeField(
        verbose_name='Added',
        auto_now_add=True
    )

    class Meta:
        abstract = True


class Location(StatusModel):
    name = models.CharField(
        max_length=constants.MAX_LENGTH,
        verbose_name='Place name',
    )

    class Meta:
        verbose_name = 'location'
        verbose_name_plural = 'Locations'

    def __str__(self):
        return self.name[:constants.MAX_LEN]


class Category(StatusModel):
    title = models.CharField(
        max_length=constants.MAX_LENGTH,
        verbose_name='Title'
    )
    description = models.TextField(
        verbose_name='Description'
    )
    slug = models.SlugField(
        max_length=64,
        unique=True,
        verbose_name='ID',
        help_text=('The page ID for the URL; '
                   'latin characters, numbers, ',
                   'hyphens and underscores are allowed.')
    )

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title[:constants.MAX_LEN]


class Post(StatusModel):
    title = models.CharField(
        max_length=constants.MAX_LENGTH,
        verbose_name='Title'
    )
    text = models.TextField(verbose_name='Text')
    pub_date = models.DateTimeField(
        verbose_name='Date and time of publication',
        help_text=('If you set a date and time in the future, ',
                   'you can make deferred publications.')
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='The author of the publication',
        related_name='posts'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Location',
        related_name='posts'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Category',
        related_name='posts'
    )
    image = models.ImageField(
        'The picture of the publication',
        blank=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'publication'
        verbose_name_plural = 'Publications'

    def comment_count(self):
        return self.comments.count()

    def __str__(self):
        return self.title[:constants.MAX_LEN]

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[str(self.id)])


class Comment(StatusModel):
    text = models.TextField('The text of the comment')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('created_at',)
