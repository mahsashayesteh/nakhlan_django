from django.db import models
from django.urls import reverse


# Create your models here.

class MainCategory(models.Model):
    name = models.CharField(max_length=100, default='null', verbose_name='نام')
    slug = models.SlugField(max_length=250, unique=True, allow_unicode=True, db_collation='utf8_persian_ci', null=True)
    description = models.CharField(max_length=255, blank='True', verbose_name="توضیحات")
    cat_image = models.ImageField(upload_to='photos/categories', blank=True, verbose_name="عکس دسته بندی")

    class Meta:
        verbose_name = 'maincategory'
        verbose_name_plural = 'maincategories'

    def get_url(self):
        return reverse('products_by_main_category', args=[self.slug])

    def __str__(self):
        return self.name


class Category(models.Model):
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE, null=True, verbose_name="دسته بندی اصلی")
    name = models.CharField(max_length=100, verbose_name='نام')
    slug = models.SlugField(max_length=250, unique=True, allow_unicode=True, db_collation='utf8_persian_ci', null=True)
    image = models.ImageField(upload_to='photos/banner_category', verbose_name='عکس بنر برای صفحه اصلی', blank=True)

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
    slug = models.SlugField(max_length=250, unique=True, allow_unicode=True, db_collation='utf8_persian_ci', null=True)
    image = models.ImageField(upload_to='photos/banner_sub_category', verbose_name='عکس بنر برای صفحه اصلی', blank=True)
    description_update_image = models.TextField(max_length=512, verbose_name='توضیحات بارگیری عکس ', default='272*140')

    def get_url(self):
        return reverse('products_by_sub_category', args=[self.slug])

    def __str__(self):
        return self.category.main_category.name + '----' + self.category.name + '----' + self.name


class BlogMainCategory(models.Model):
    name = models.CharField(max_length=100, default='null', verbose_name='نام', unique=True, db_collation='utf8_persian_ci')
    slug = models.SlugField(max_length=250, unique=True, allow_unicode=True, db_collation='utf8_persian_ci', null=True)
    cat_image = models.ImageField(upload_to='photos/categories', blank=True, verbose_name="عکس دسته بندی")

    class Meta:
        verbose_name = 'blogsmaincategory'
        verbose_name_plural = 'blogs main categories'

    def get_url(self):
        return reverse('blogs_by_main_category', args=[self.slug])

    def __str__(self):
        return self.name


class BlogCategory(models.Model):
    blog_main_category = models.ForeignKey(BlogMainCategory, on_delete=models.CASCADE, null=True, verbose_name="دسته بندی اصلی")
    name = models.CharField(max_length=100, verbose_name='نام', unique=True, db_collation='utf8_persian_ci')
    slug = models.SlugField(max_length=250, unique=True, allow_unicode=True, db_collation='utf8_persian_ci', null=True)

    def get_url(self):
        return reverse('blogs_by_category', args=[self.slug])

    class Meta:
        verbose_name = 'blogcategory'
        verbose_name_plural = 'blog categories'

    def __str__(self):
        return self.name

# class BlogSubCategory(models.Model):
#     blog_category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, null=True, verbose_name='دسته بندی')
#     name = models.CharField(max_length=100, verbose_name='نام',unique=True,db_collation='utf8_persian_ci' )
#     slug=models.SlugField(max_length=250,unique=True,allow_unicode=True,db_collation='utf8_persian_ci',null=True)
#
#     def get_url(self):
#         return reverse('blogs_by_sub_category', args=[self.slug])
#
#     def __str__(self):
#         return self.category.main_category.name + '----' + self.category.name + '----' +self.name
