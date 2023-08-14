from django.contrib import admin
from .models import MainCategory, Category, SubCategory
from store.models import Product
from mptt.admin import DraggableMPTTAdmin


# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')



admin.site.register(MainCategory)
admin.site.register(SubCategory)
admin.site.register(Category, CategoryAdmin)
