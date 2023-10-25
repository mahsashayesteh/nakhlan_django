from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.template.loader import render_to_string
from django.db.models import Max, Min

import category.models
from .models import Product, ReviewRating, ProductGallery, BrandsName, Section
from carts.models import Cart, CartItem
from category.models import MainCategory, Category, SubCategory
from django.http import HttpResponse, JsonResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.contrib import messages
from jalali_date import datetime2jalali, date2jalali
import mysql.connector

from carts.views import _cart_id
from .forms import ReviewForm

from ajax_select import LookupChannel

# Create your views here.

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="ecommerce_website"
)
mycursor = mydb.cursor()
def Avg(product):
    fetch_reviews = (
        "SELECT AVG(rating) as avgrating, COUNT(rating) as countrating FROM ecommerce_website.store_reviewrating  WHERE "
        "status=1 and product_id=%s;")
    mycursor.execute(fetch_reviews, [product.id])
    reviews_sql = mycursor.fetchall()

    if reviews_sql is not None:
        count = reviews_sql[0][1]
        avg = reviews_sql[0][0]
        return avg, count

def store(request, main_category_slug=None, category_slug=None, sub_category_slug=None, ):
    brands = BrandsName.objects.all()

    categories = None
    products = None
    min_price = Product.objects.all().aggregate(Min('price'))
    max_price = Product.objects.all().aggregate(Max('price'))

    FilterPrice = request.GET.get('FilterPrice')
    filter_section = Section.objects.filter().all()

    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)

        for product in products:
            product.avg = Avg(product)[0]
            product.count_review = Avg(product)[1]
        paginator = Paginator(products, 8)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    elif main_category_slug is not None:
        main_categories = get_object_or_404(MainCategory, slug=main_category_slug)
        products = Product.objects.filter(category__main_category=main_categories, is_available=True)

        for product in products:
            product.avg = Avg(product)[0]
            product.count_review = Avg(product)[1]
        paginator = Paginator(products, 8)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    elif sub_category_slug is not None:

        sub_categories = get_object_or_404(SubCategory, slug=sub_category_slug)
        products = Product.objects.filter(sub_category=sub_categories, is_available=True)

        for product in products:
            product.avg = Avg(product)[0]
            product.count_review = Avg(product)[1]
        paginator = Paginator(products, 8)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    elif FilterPrice:
        Int_FilterPrice = int(FilterPrice)
        products = Product.objects.filter(price__lte=Int_FilterPrice)

        for product in products:
            product.avg = Avg(product)[0]
            product.count_review = Avg(product)[1]
        paginator = Paginator(products, 8)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        for product in products:
            product.avg = Avg(product)[0]
            product.count_review = Avg(product)[1]
        paginator = Paginator(products, 8)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,
        'brands': brands,
        'min_price': min_price,
        'max_price': max_price,
        'FilterPrice': FilterPrice,
        'filter_sec': filter_section,
    }

    return render(request, 'store/store.html', context)


def filter_sec(request):
    filter_section = Section.objects.filter().all()
    sec = request.GET.getlist('filter_category')
    allProducts = Product.objects.all().order_by('-id').distinct()
    if len(sec) > 0:
        allProducts = allProducts.filter(section__id__in=sec).distinct()
        for product in allProducts:
            product.avg = Avg(product)[0]
            product.count_review = Avg(product)[1]
        paginator = Paginator(allProducts, 8)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = allProducts.count()

    contex = {
        'products': paged_products,
        'product_count': product_count,
        'product': allProducts,
        'filter_sec': filter_section,
    }

    t = render_to_string('store/ajax/product.html', contex)
    # t1 = render_to_string('store/ajax/paginator.html', {'products': paged_products,'product_count': product_count, })

    return JsonResponse({'data': t}, )



def filter_data(request):
    categories = request.GET.getlist('category[]')
    brands = request.GET.getlist('brand[]')
    filter_section = Section.objects.filter().all()
    allProducts = Product.objects.all().order_by('-id').distinct()
    if len(categories) > 0:
        allProducts = allProducts.filter(category__id__in=categories).distinct()
        for product in allProducts:
            product.avg = Avg(product)[0]
            product.count_review = Avg(product)[1]
        paginator = Paginator(allProducts, 8)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = allProducts.count()


    if len(brands) > 0:
        allProducts = allProducts.filter(brand__id__in=brands).distinct()
        for pro in allProducts:
            pro.avg = Avg(pro)[0]
            pro.count_review = Avg(pro)[1]
        paginator = Paginator(allProducts, 8)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = allProducts.count()


    context = {
        'products': paged_products,
        'product_count': product_count,
        'product': allProducts,
        'filter_sec': filter_section,
    }

    t = render_to_string('store/ajax/product.html', context)

    return JsonResponse({'data': t})





def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),
                                          product=single_product).exists()

    except Exception as e:
        raise e
    # گرفتن میانگین و تعداد دیدگاه های درج شده برای محصولات
    fetch_reviews = (
        "SELECT AVG(rating) as avgrating, COUNT(rating) as countrating FROM ecommerce_website.store_reviewrating  WHERE "
        "status=1 and product_id=%s;")
    mycursor.execute(fetch_reviews, [single_product.id])
    reviews_sql = mycursor.fetchall()

    avg = 0
    count = 0
    if reviews_sql is not None:
        count = reviews_sql[0][1]
        avg = reviews_sql[0][0]

    # در اینجا می توان try , except قرارداد جهت اینکه بررسی کنیم کاربر محصول را خریده یا خیر اگر
    # خریده بود بتواند دیدگاه خود را ثبت کند

    # بدست آوردن دیدگاه ها جهت قراردادن در صفحات
    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)
    reviews_exist = ReviewRating.objects.filter(product_id=single_product.id, status=True).exists()
    get_review = ''
    if reviews_exist:
        get_review = ReviewRating.objects.filter(product_id=single_product.id, status=True)

    for review in get_review:
        review.update_at = datetime2jalali(review.update_at).strftime('%Y/%m/%d')

    # بدست آوردن عکس های گالری محصول
    product_gallery = ProductGallery.objects.filter(product=single_product.id)

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'reviews': reviews,
        'product_gallery': product_gallery,
        'avg': avg,
        'count': count,
    }
    return render(request, 'store/product_detail.html', context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(
                Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)


def submit_review(request, product_id):
    url = request.META['HTTP_REFERER']

    if request.method == "POST":
        exits_reviews = ReviewRating.objects.filter(user__id=request.user.id,
                                                    product__id=product_id).exists()
        if exits_reviews:
            reviews = ReviewRating.objects.filter(user__id=request.user.id,
                                                  product__id=product_id).first()
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'متشکریم! دیدگاه شما به روز رسانی شد.')
            return redirect(url)

        elif exits_reviews is not True:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                cd = form.cleaned_data
                data.subject = cd['subject']
                data.review = cd['review']
                data.rating = cd['rating']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'متشکریم!! دیدگاه شما ارسال شد.')
                return redirect(url)
            else:
                messages.error(request, 'لطفا بخش امتیاز دهی (⭐) را تکمیل نمایید. با تشکر')
                return redirect(url)
    else:
        return render(request, url)

