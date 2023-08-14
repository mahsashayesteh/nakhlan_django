from .models import MainCategory, Category, SubCategory

def menu_links(request):
    main_categories = MainCategory.objects.all()
    categories = Category.objects.all()
    return dict(main_categories=main_categories, categories=categories)
