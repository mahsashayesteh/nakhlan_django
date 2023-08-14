from django.shortcuts import render, redirect
from django.http import HttpResponse
from carts.models import CartItem

from .forms import OrderForms
from .models import Order
import datetime
from django.contrib import messages

# Create your views here.

def payments(request):

    
    return render(request, 'orders/payments.html')

def place_order(request, quantity=0, total=0, ):
    current_user = request.user

    # if the cart count is less than or equal zero back to shop
    cart_items = CartItem.objects.filter(user= current_user)
    cart_count = cart_items.count()
    if cart_count <=0:
        return redirect('store')
    
    for cart_item in cart_items:
        total += (cart_item.product.price *cart_item.quantity)
        quantity += cart_item.quantity
    
    if request.method =="POST":
        form = OrderForms(request.POST)
        
        if form.is_valid():
             
        # store all billing information inside order table
            #  cd = form.cleaned_data
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.zip_code = form.cleaned_data['zip_code']
            data.email = form.cleaned_data['email']
            data.address = form.cleaned_data['address']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = total
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
             
             #generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") #20210305
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order':order,
                'cart_items':cart_items,
                'total':total,
            }
            return render(request, 'orders/payments.html', context)
        else:
           messages.error(request, 'مشکلی در ثبت اطلاعات پیش آمده است.')
           return redirect('checkout') 
             
           
