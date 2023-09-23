from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse
from django_quill.fields import QuillField
from jalali_date import datetime2jalali
from taggit.managers import TaggableManager
from accounts.models import Account
from category.models import BlogCategory, BlogMainCategory


# Create your models here.


class BlogDetails(models.Model):
    choices = (
        ('disable', 'غیرفعال'),
        ('active', 'فعال'),
        ('editing', 'در حال ویرایش')
    )
    subject = models.CharField(max_length=225,unique=True, db_collation='utf8_persian_ci')
    slug = models.SlugField(max_length=250, unique=True, allow_unicode=True, db_collation='utf8_persian_ci', null=True)
    description = QuillField(default='null')
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=choices, default='disable')
    img_banner = models.ImageField(upload_to='blogs/blog_details_banner', verbose_name='تصویر بنر بلاگ', null=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, null=True)
    # sub_category = models.ForeignKey(BlogSubCategory, on_delete=models.CASCADE, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    tags = TaggableManager()

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'blogdetails',
        verbose_name_plural = 'Blog Details'

    def get_url(self):
        return reverse('blogs', args=[self.category.slug, self.slug])

