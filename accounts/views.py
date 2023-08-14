from django.shortcuts import render, redirect, HttpResponse
from jalali_date import datetime2jalali

from .forms import RegisterationForm, UserProfileForm, UserForm
from .models import Account, UserProfile
from orders.models import Order, OrderProduct
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from carts.views import _cart_id
from carts.models import Cart, CartItem

# verifiacation_email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404

import requests

# connect to database
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="ecommerce_website"
)
mycursor = mydb.cursor()




# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegisterationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            first_name = cd['first_name']
            last_name = cd['last_name']
            phone_number = cd['phone_number']
            email = cd['email']
            password = cd['password']
            username = email.split('@')[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name,
                                               email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()

            # USER ACTIVATION
            current_site = get_current_site(request)
            main_subject = 'لطفا حساب کاربری خود را فعال کنید'
            message = render_to_string('accounts/account_verifiaction_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(main_subject, message, to=[to_email])
            send_email.send()
            messages.success(request, 'ثبت نام شما با موفقیت انجام شد.')
            return redirect('/accounts/login/?command=verification&email=' + email)

    else:
        form = RegisterationForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exits = CartItem.objects.filter(cart=cart).exists()

                if is_cart_item_exits:
                    cart_item = CartItem.objects.filter(cart=cart)
                    product_variation = []

                    for item in cart_item:
                        variation = item.variation.all()
                        product_variation.append(list(variation))

                    ex_var_list = []
                    id_login = []
                    cart_item = CartItem.objects.filter(user=user)
                    for item in cart_item:
                        exist_variation = item.variation.all()
                        ex_var_list.append(list(exist_variation))
                        id_login.append(item.id)

                    for pr in product_variation:
                        if pr in ex_var_list:

                            index = ex_var_list.index(pr)
                            item_id = id_login[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()


            except:
                pass
            auth.login(request, user)
            messages.success(request, 'شما وارد شدید')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    next_page = params['next']
                    return redirect(next_page)
            except:

                return redirect('dashboard')

        else:
            messages.error(request, 'ورود نامعتبر!')
            return redirect('login')
    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'شما خارج شدید.')
    return render(request, 'accounts/login.html')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        # messages.success(request, '.با تشکر از شما برای ثبت نام با ما. ما یک ایمیل تأیید به
        # آدرس ایمیل شما ارسال کرده ایم. لطفا آن را تأیید کنید')
        return redirect('login')
    else:
        messages.error(request, 'لینک فعال سازی نامعتبر است.')


@login_required(login_url='login')
def dashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()
    userprofile = UserProfile.objects.get_or_create(user=request.user)[0]
    print(userprofile)

    context = {
        'orders_count': orders_count,
        'userprofile': userprofile,
    }
    return render(request, 'accounts/dashboard.html', context)


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            # REST PASSWORD EMAIL
            current_site = get_current_site(request)
            main_subject = 'باز نشانی رمز عبور'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(main_subject, message, to=[to_email])
            try:
                send_email.send()
                messages.success(request, 'لینک بازیابی رمز عبور به ایمیل شما ارسال شد.')
                return redirect('login')
            except:
                messages.error(request, 'لطفا دوباره تلاش کنید!!')

        else:
            messages.error(request, 'حساب کاربری با ایمیل وارد شده وجود ندارد.')
            return redirect('forgotPassword')

    return render(request, 'accounts/forgotPassword.html', {})


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'لطفا رمز عبور را بازنشانی کنید.')
        return redirect('resetPassword')
    else:
        messages.error(request, 'لینک فعال سازی نامعتبر است.')
        return redirect('login')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['Password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')

            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, '.تغییر رمز عبور موفقیت آمیز بود')
            return redirect('login')

        else:
            messages.error(request, '!رمز عبور مطابقت ندارد')
            return redirect('resetPassword')

    return render(request, 'accounts/resetPassword.html')


@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')

    for order in orders:
        order.created_at = datetime2jalali(order.created_at).strftime('%Y/%m/%d, %H:%M')

    context = {
        'orders': orders,

    }
    return render(request, 'accounts/my_orders.html', context)


@login_required(login_url='login')
def edit_profile(request):
    use_pro2 = UserProfile.objects.get_or_create(user=request.user)[0]
    use_pro = get_object_or_404(UserProfile, user=request.user)


    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)

        profile_form = UserProfileForm(request.POST, request.FILES, instance=use_pro)


        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'پروفایل شما با موفقیت به روز رسانی شد.')
            return redirect('edit_profile')
    else:


        user_form = UserForm(instance=request.user)

        if use_pro2:


            profile_form = UserProfileForm(instance=use_pro2)
        else:
            profile_form = UserProfileForm()
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'use_pro': use_pro,
    }
    return render(request, 'accounts/edit_profile.html', context)


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)
        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'رمز عبور شما با موفقیت به روزرسانی شد')
                return redirect('change_password')
            else:
                messages.error(request, 'لطفا رمز عبور فعلی را به درستی وارد کنید.')
                return redirect('change_password')
        else:
            messages.error(request, 'رمز عبور مطابقت ندارد.')
            return redirect('change_password')
    return render(request, 'accounts/change_password.html')


@login_required(login_url='login')
def order_detail(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    for item in [order]:
        item.created_at = datetime2jalali(item.created_at).strftime('%Y/%m/%d, %H:%M')
    context = {
        'order_detail': order_detail,
        'order': order,
    }
    return render(request, 'accounts/order_detail.html', context)






