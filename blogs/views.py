from jalali_date import datetime2jalali

from .models import BlogDetails
from django.shortcuts import get_object_or_404, render
from django.utils.encoding import uri_to_iri
# Create your views here.
from django.template.loader import render_to_string


def blog(request):
    blogs = BlogDetails.objects.order_by('-update_date').filter(status='active')
    print(blogs)
    context = {
        'blogs': blogs,
    }
    return render(request, 'blogs/blogs.html', context)


def blog_details(request, slug, category_slug):
    blogs = get_object_or_404(BlogDetails, slug=uri_to_iri(slug), category__slug=uri_to_iri(category_slug))
    blogs.update_date =datetime2jalali(blogs.update_date).strftime('%Y/%m/%d')
    context={
        'blogs':blogs,
    }
    return render(request, 'blogs/blog_details.html', context)
