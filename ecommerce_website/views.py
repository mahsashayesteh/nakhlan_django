from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from carts.models import CartItem, Cart
from carts.views import _cart_id
from store.models import Product, ReviewRating, Variation, Slider
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="ecommerce_website"
)
mycursor = mydb.cursor()

sliders = []
def home(request):
    global sliders

    products = Product.objects.all().filter(is_available=True).order_by('created_date')
    product_special_offer = Product.objects.all().filter( section__name_show='special offer').order_by('created_date')

    for product in product_special_offer:

        sliders = Slider.objects.all()

        fetch_reviews = (
            "SELECT AVG(rating) as avgrating, COUNT(rating)  as count_rating FROM ecommerce_website.store_reviewrating  WHERE "
            "status=1 and product_id={};").format(product.id)
        mycursor.execute(fetch_reviews)
        reviews_sql = mycursor.fetchall()
        average = 0

        if reviews_sql[0][0] is not None:
            product.average = reviews_sql[0][0]
            product.count_rating =reviews_sql[0][1]

            reviews = ReviewRating.objects.filter(product_id=product.id, status=True)
        else:
            product.average = 0
            product.count_rating = 0

    context = {
        'products': products,
        'sliders':sliders,
        'product_special_offer':product_special_offer,
    }

    return render(request, 'home.html', context)


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    current_user = request.user

    # if the user is authenticated
    if current_user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

        is_cart_item_exits = CartItem.objects.filter(product=product, user=current_user)
        if is_cart_item_exits:
            cart_item = CartItem.objects.filter(product=product, user=current_user)
            ex_var_list = []
            id = []
            for item in [cart_item]:
                existing_variation = item.variation.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                index = ex_var_list.index(product_variation)
                id_item = id[index]
                item = CartItem.objects.get(product=product, id=id_item)
                item.quantity += 1
                item.save()

            else:
                item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                if (len(product_variation) > 0):
                    item.variation.clear()
                    item.variation.add(*product_variation)
                item.save()

        else:
            item = CartItem.objects.create(product=product, quantity=1, user=current_user)
            if (len(product_variation) > 0):
                item.variation.clear()
                item.variation.add(*product_variation)
            item.save()

        return redirect('cart')

    # if the user is not authenticated
    else:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()

        is_cart_item_exits = CartItem.objects.filter(product=product, cart=cart).exists()

        if is_cart_item_exits:
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variation.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                index = ex_var_list.index(product_variation)
                id_item = id[index]
                item = CartItem.objects.get(product=product, id=id_item)
                item.quantity += 1

                item.save()


            else:
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                if (len(product_variation) > 0):
                    item.variation.clear()
                    item.variation.add(*product_variation)
                item.save()

        else:
            item = CartItem.objects.create(product=product, quantity=1, cart=cart)
            if (len(product_variation) > 0):
                item.variation.clear()

                item.variation.add(*product_variation)
            item.save()

        return redirect('cart')


def about_us(request):
    return render(request, 'Interactions/about_us.html')


def contact_us(request):
    return render(request, 'Interactions/contact_us.html')
