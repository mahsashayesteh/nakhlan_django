from .models import MainCategory, Category, SubCategory, BlogMainCategory, BlogCategory

def menu_links(request):
    main_categories = MainCategory.objects.all()
    categories = Category.objects.all()
    sub_category = SubCategory.objects.all()
    blog_main_category = BlogMainCategory.objects.all()
    blog_category = BlogCategory.objects.all()
    return dict(main_categories=main_categories, categories=categories, sub_categories=sub_category, blog_category=blog_category, blog_main_categories=blog_main_category)
