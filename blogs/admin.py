from django.contrib import admin
from jalali_date import datetime2jalali

from .models import BlogDetails


# Register your models here.
class AdminBlogDetails(admin.ModelAdmin):
    list_filter = ('likes', 'views', 'created_date', 'update_date', 'author')
    list_display = ('subject', 'likes', 'views', 'shamsi_created_date', 'shamsi_update_date', 'author')
    prepopulated_fields = {"slug": ("subject",)}

    @admin.display(description='زمان ایجاد')
    def shamsi_created_date(self, obj):
        return datetime2jalali(obj.created_date).strftime('%H:%M _ %Y/%m/%d')

    shamsi_created_date.admin_order_field = 'created_date'

    @admin.display(description='زمان به روز رسانی')
    def shamsi_update_date(self, obj):
        return datetime2jalali(obj.update_date).strftime('%H:%M _ %Y/%m/%d')

    shamsi_created_date.admin_order_field = 'update_date'

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()


admin.site.register(BlogDetails, AdminBlogDetails)
