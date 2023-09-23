from django.contrib import admin
from django.template.loader_tags import register

from .models import Product, Variation, ReviewRating, ProductGallery, Additional_Infomation, Section, BrandsName, Slider
from jalali_date import datetime2jalali
import admin_thumbnails



# Register your models here.
@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 4

class AdditionalInformationTabular(admin.TabularInline):
    model = Additional_Infomation
    extra = 4

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'sub_category', 'shamsi_date_created', 'shamsi_date_modified', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    inlines = (ProductGalleryInline, AdditionalInformationTabular,)
    list_editable = ('category', 'sub_category')

    # show date in shamsi format
    @admin.display(description='زمان ایجاد')
    def shamsi_date_created(self, obj):
        return datetime2jalali(obj.created_date).strftime('%H:%M _ %Y/%m/%d')

    shamsi_date_created.admin_order_field = 'created_date'

    # show date in shamsi format
    @admin.display(description='زمان تغییر')
    def shamsi_date_modified(self, obj):
        return datetime2jalali(obj.modified_date).strftime('%H:%M _ %Y/%m/%d')

    shamsi_date_modified.admin_order_field = 'modified_date'


class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active', 'created_date')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_value', 'is_active')
    readonly_fields = ('created_date',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'subject', 'rating', 'status', 'get_create_date', 'get_update_date')
    list_editable = ('status',)
    list_filter = ('product', 'user', 'subject', 'rating', 'status', 'created_at', 'update_at')
    readonly_fields = ('get_create_date', 'get_update_date')

    # show date in shamsi format
    # @admin.display(description='تاریخ به روزرسانی')
    def get_update_date(self, obj):
        return datetime2jalali(obj.update_at).strftime('%H:%M _ %Y/%m/%d')

    get_update_date.admin_order_field = 'update_at'

    # show date in shamsi format
    # @admin.display(description='تاریخ ایجاد')
    def get_create_date(self, obj):
        return datetime2jalali(obj.created_at).strftime('%H:%M _ %Y/%m/%d')

    get_create_date.admin_order_field = 'created_at'

class SliderAdmin(admin.ModelAdmin):
    list_display = ( 'product', 'discount_deal')

    list_filter = ('product', 'discount_deal')


admin.site.register(Product, ProductAdmin)
admin.site.register(Additional_Infomation)
admin.site.register(Section)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating, ReviewAdmin)
admin.site.register(ProductGallery)
admin.site.register(BrandsName)
admin.site.register(Slider, SliderAdmin)