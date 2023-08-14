from django.db import models
from accounts.models import Account
from store.models import Product, Variation


# Create your models here.


class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='کاربر')
    payment_id = models.CharField(max_length=100, verbose_name='شناسه پرداخت')
    payment_method = models.CharField(max_length=100, verbose_name='روش پرداخت')
    amount_paid = models.CharField(max_length=100, verbose_name='مقدار پرداخت')
    status = models.CharField(max_length=100, verbose_name='وضعیت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان  ایجاد')

    def __str__(self):
        return self.payment_id


class Order(models.Model):
    STATUS = (
        ('New', 'جدید'),
        ('Accepted', 'پذیرفته شده'),
        ('Completed', 'تکمیل شده'),
        ('Cancelled', 'لغو شئده'),
    )

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, verbose_name='کاربر')
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='پرداخت')
    order_number = models.CharField(max_length=100, verbose_name='شماره سفارش')
    first_name = models.CharField(max_length=70, verbose_name='نام')
    last_name = models.CharField(max_length=70, verbose_name='نام خانوادگی')
    phone = models.CharField(max_length=15, verbose_name='تلفن')
    email = models.EmailField(max_length=70, verbose_name='ایمیل')
    address = models.CharField(max_length=256, verbose_name='نشانی گیرنده')
    zip_code = models.CharField(max_length=15, default='0', verbose_name='کد پستی')
    order_note = models.CharField(max_length=100, null=True, verbose_name='متن سفارش')
    order_total = models.FloatField(verbose_name='تعداد سفارش')
    status = models.CharField(max_length=20, choices=STATUS, default='New', verbose_name='وضعیت')
    ip = models.CharField(blank=True, max_length=20, )
    is_ordered = models.BooleanField(default=False, verbose_name='سفارش داده شده')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.first_name


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='سفارش')
    Payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='پرداخت')
    user = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='کاربر')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='کالا')
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE, verbose_name='تنوع')
    color = models.CharField(max_length=70, verbose_name=' رنگ')
    size = models.CharField(max_length=50, verbose_name='سایز')
    quantity = models.IntegerField(verbose_name='تعداد')
    product_price = models.FloatField(verbose_name='هزینه کالا')
    ordered = models.BooleanField(default=False, verbose_name='سفارش داده شده')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name
