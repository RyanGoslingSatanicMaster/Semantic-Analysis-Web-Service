from django.contrib import admin
from django.urls import path, include
from publish.views import view_post

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path(r'^admin/', admin.site.urls),
    path(r'^(?P<slug>[a-zA-Z0-9\-]+)', view_post, name='view_post')
]
