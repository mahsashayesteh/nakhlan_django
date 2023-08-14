from django.db import models
from django.urls import reverse



# Create your models here.
class MainCategory(models.Model):
    name = models.CharField(max_length=100, default='null',verbose_name= 'نام')
    slug = models.SlugField(max_length=100, unique=True)
    description = models.CharField(max_length=255, blank='True', verbose_name= "توضیحات")
    cat_image = models.ImageField(upload_to='photos/categories', blank=True, verbose_name="عکس دسته بندی")


    class Meta:
        verbose_name = 'maincategory'
        verbose_name_plural = 'maincategories'

    def get_url(self):
        return reverse('products_by_main_category', args=[self.slug])

    def __str__(self):
        return self.name


class Category(models.Model):
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE, null=True ,verbose_name="دسته بندی اصلی")
    name = models.CharField(max_length=100, verbose_name='نام')
    slug = models.SlugField(max_length=100, unique=True)


    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, verbose_name='دسته بندی')
    name = models.CharField(max_length=100, verbose_name='نام')
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True)

    def get_url(self):
        return reverse('products_by_sub_category', args=[self.slug])

    def __str__(self):
        return self.category.main_category.name + '----' + self.category.name + '----' +self.name
