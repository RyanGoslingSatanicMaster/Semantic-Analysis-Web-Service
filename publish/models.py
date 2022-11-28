from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model


class Post(models.Model):
    created = models.DateTimeField('Created Date', default=timezone.now)
    title = models.CharField('Title', max_length=200)
    content = models.TextField('Content')
    slug = models.SlugField('Slug')

    def __str__(self):
        return '"%s" by %s' % (self.title, self.author)