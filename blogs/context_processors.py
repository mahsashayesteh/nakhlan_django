from django.shortcuts import get_object_or_404
from jalali_date import datetime2jalali

from .models import BlogDetails


def menu_links(request):
    blogs = BlogDetails.objects.filter(status='active')
    for blog in blogs:
        blog.update_date = datetime2jalali(blog.update_date).strftime('%Y/%m/%d')

    return dict(blogs=blogs, )
