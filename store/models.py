import mysql.connector

from django.db import models
from django_quill.fields import QuillField

from category.models import Category, MainCategory, SubCategory
from django.urls import reverse
from accounts.models import Account, UserProfile


from django_jalali.db import models as jmodels
from django.db.models import Avg


# ارتباط مستقیم با دیتابیس
# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   password="1234",
#   database="ecommerce_website"
# )
# mycursor = mydb.cursor()
# Create your models here.

class Section(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام")
    name_show = models.CharField(max_length=100, verbose_name="نام_جهت نمایش", default='null')

    def __str__(self):
        return self.name


class BrandsName(models.Model):
    name = models.CharField(max_length=250)
    is_available = models.BooleanField(default=True, verbose_name="فعال است")

    def __str__(self):
        return self.name


class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True, verbose_name="نام کالا")
    slug = models.SlugField(max_length=200, unique=True)
    brand = models.ForeignKey(BrandsName, on_delete=models.DO_NOTHING, null=True)
    product_information = QuillField(null=True, verbose_name="اطلاعات کالا", blank=True)
    description = QuillField(blank=True, verbose_name="توضیحات", null=True)
    price = models.IntegerField(verbose_name="قیمت")
    discount = models.IntegerField(null=True, verbose_name="تخفیف")
    tags = models.CharField(max_length=100, null=True, verbose_name="تگ")
    images = models.ImageField(upload_to='photos/products', verbose_name="عکس ها")
    stock = models.IntegerField(verbose_name="موجودی")
    section = models.ForeignKey(Section, on_delete=models.DO_NOTHING, null=True, verbose_name="قسمت")
    is_available = models.BooleanField(default=True, verbose_name="موجود")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, verbose_name="دسته بندی")
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, verbose_name="دسته بندی")
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name


class Additional_Infomation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="کالا")
    specification = models.CharField(max_length=100, verbose_name="مشخصات")
    detail = models.CharField(max_length=100, verbose_name="جزئیات")


class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)


variation_category_choices = (
    ('رنگ', 'رنگ'),
    ('سایز', 'سایز'),
)


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="کالا")
    variation_category = models.CharField(max_length=100, choices=variation_category_choices, verbose_name="دسته بندی تنوع")
    variation_value = models.CharField(max_length=100, verbose_name="مقدار تنوع")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    created_date = models.DateTimeField(auto_now_add=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="کالا")
    user = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name="کاربر ")

    subject = models.CharField(max_length=256, blank=True, verbose_name="موضوع")
    review = models.TextField(max_length=500, blank=True, verbose_name="دیدگاه")
    rating = models.FloatField(verbose_name="رتبه بندی")
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True, verbose_name="وضعیت")
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE, verbose_name="کالا")
    image = models.ImageField(upload_to='store/products', max_length=225, verbose_name="عکس")

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name = 'productgallery',
        verbose_name_plural = 'product gallery'


class Slider(models.Model):
    discount_deal = (
        ('پیشنهاد ویژه', 'پیشنهاد ویژه'),
        ('جدیدترین ها', 'جدیدترین ها'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="کالا", default=None)
    image = models.ImageField(upload_to='photos/slider_imgs')
    discount_deal = models.CharField(choices=discount_deal, max_length=100, default=0)

    def __str__(self):
        return self.product.product_name
