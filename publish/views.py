from django.http import Http404
from django.shortcuts import render
from .models import Post


def view_post(request, slug):
    try:
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        raise Http404("Poll does not exist")

    return render(request, 'post.html', context={'post': post})
# Create your views here.
