from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, Variation
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required


# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def discount():
    products = Product.objects.filter(status=True)
    for i in products:
        if i.discount > 0:
            price = i.price - (i.price * i.discount / 100)
        else:
            price = i.price

    return price


def add_cart(request, product_id, ):
    product = Product.objects.get(id=product_id)
    current_user = request.user

    # if the user is authenticated
    if current_user.is_authenticated:
        product_variation = []
        if request.method == 'POST':

            quantity = request.POST['quantity']
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
            for item in cart_item:
                if item.variation is not None and item.variation is not '':
                    existing_variation = item.variation.all()
                    ex_var_list.append(list(existing_variation))
                    id.append(item.id)

            if product_variation in ex_var_list:
                index = ex_var_list.index(product_variation)
                id_item = id[index]
                item = CartItem.objects.get(product=product, id=id_item)
                item.quantity += int(quantity)
                item.save()

            else:
                item = CartItem.objects.create(product=product, quantity=quantity, user=current_user)
                if len(product_variation) > 0:
                    item.variation.clear()
                    item.variation.add(*product_variation)
                item.save()

        else:
            item = CartItem.objects.create(product=product, quantity=quantity, user=current_user)
            if len(product_variation) > 0:
                item.variation.clear()
                item.variation.add(*product_variation)
            item.save()

        return redirect('cart')

    # if the user is not authenticated
    else:
        product_variation = []

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
        quantity = request.POST['quantity']
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

            item.quantity += int(quantity)
            item.save()


        else:

            item = CartItem.objects.create(product=product, quantity=quantity, cart=cart)
            if len(product_variation) > 0:
                item.variation.clear()
                item.variation.add(*product_variation)
            item.save()

    else:
        quantity = request.POST['quantity']
        item = CartItem.objects.create(product=product, quantity=quantity, cart=cart)
        if len(product_variation) > 0:
            item.variation.clear()

            item.variation.add(*product_variation)
        item.save()

    return redirect('cart')


def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)

    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


def cart(request, quantity=0, sub_total=0, shipping_cost=38000, total=0, cart_items=None):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            quantity += cart_item.quantity
            if cart_item.product.discount > 0:
                price = cart_item.product.price
                discount_product = cart_item.product.discount
                discount_price = price - (price * discount_product / 100)
                sub_total += (discount_price * cart_item.quantity)
                total = sub_total + cart_item.shipping_cost
                shipping_cost = cart_item.shipping_cost
            else:
                sub_total += (cart_item.product.price * cart_item.quantity)
                total = sub_total + cart_item.shipping_cost
                shipping_cost = cart_item.shipping_cost

    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'sub_total': sub_total,
        'shipping_cost': shipping_cost,

    }
    return render(request, 'store/cart.html', context)


@login_required(login_url='login')
def checkout(request, sub_total=0, shipping_cost=38000, quantity=0, total=0, cart_items=None):
    tax = 0
    grand_total = 0
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            sub_total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        total = sub_total + cart_item.shipping_cost
        shipping_cost = cart_item.shipping_cost
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'sub_total': sub_total,
        'quantity': quantity,
        'cart_items': cart_items,
        'shipping_cost': shipping_cost,

    }
    return render(request, 'store/checkout.html', context)
