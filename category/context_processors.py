from .models import Category

def menu_links(requst):
    links = Category.objects.all()
    return dict(links = links)
