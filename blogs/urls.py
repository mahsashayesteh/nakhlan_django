from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.blog, name='blog'),
    re_path(r'Blog_category/(?P<category_slug>[-\w]+)/(?P<slug>[-\w]+)/', views.blog_details, name='blogs'),
    re_path(r'filter_blogs/', views.filter_ajax, name='ajax-filter-blogs'),
]
