from django.contrib import admin
from .models import MainCategory, Category, SubCategory, BlogMainCategory, BlogCategory
from store.models import Product
from mptt.admin import DraggableMPTTAdmin


# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')

class BlogCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')

class BlogMainCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')

# class BlogSubCategoryAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug': ('name',)}
#     list_display = ('name', 'slug')


admin.site.register(MainCategory)
admin.site.register(SubCategory)
admin.site.register(Category, CategoryAdmin)
admin.site.register(BlogMainCategory, BlogMainCategoryAdmin)
admin.site.register(BlogCategory, BlogCategoryAdmin)