from django.db import models
from store.models import Product, Variation
from accounts.models import Account


# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=225, blank=True)
    date_add = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, verbose_name="کاربر")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="محصول")
    variation = models.ManyToManyField(Variation, blank=True, verbose_name="تنوع")
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(verbose_name="تعداد")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    shipping_cost = models.IntegerField(default=38000, verbose_name="هزینه حمل و نقل")

    # def sub_total(self):
    #
    #     return self.quantity * self.product.price

    # def total(self):
    #
    #     return self.shipping_cost

    def __unicode__(self):
        return self.product
