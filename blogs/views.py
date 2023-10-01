from django.core.paginator import Paginator
from jalali_date import datetime2jalali
from category.models import BlogCategory
from .models import BlogDetails
from django.shortcuts import get_object_or_404, render
from django.utils.encoding import uri_to_iri
from django.http import HttpResponse, JsonResponse
# Create your views here.
from django.template.loader import render_to_string


def blog(request, category_slug=None, main_category_slug=None):
    blogs = BlogDetails.objects.order_by('-update_date').filter(status='active')
    for blog_item in blogs:
        blog_item.update_date = datetime2jalali(blog_item.update_date).strftime('%Y/%m/%d')
    paginator = Paginator(blogs, 6)
    page = request.GET.get('page')
    paged_blogs = paginator.get_page(page)
    blogs_count = blogs.count()
    context = {
        'blogs': paged_blogs,
    }
    return render(request, 'blogs/blogs.html', context)


def blog_details(request, slug, category_slug):
    blogs = get_object_or_404(BlogDetails, slug=uri_to_iri(slug), category__slug=uri_to_iri(category_slug))
    print(blogs)
    blogs.update_date = datetime2jalali(blogs.update_date).strftime('%Y/%m/%d')
    context = {
        'blogs': blogs,
    }
    return render(request, 'blogs/blog_details.html', context)


def filter_ajax(request):

    get_id_category = request.GET.getlist('filter_category_blog')
    all_blogs = BlogDetails.objects.all().order_by('-update_date').distinct()
    if len(get_id_category) > 0:
        filter_blogs = all_blogs.filter(category__id__in=get_id_category).distinct()
        paginator = Paginator(filter_blogs, 6)
        page = request.GET.get('page')
        paged_blogs = paginator.get_page(page)
    contex = {
        'blogs': paged_blogs,
        'blog': all_blogs,
    }
    t = render_to_string('blogs/ajax/blog_details.html', contex)


    return JsonResponse({'data': t}, )
