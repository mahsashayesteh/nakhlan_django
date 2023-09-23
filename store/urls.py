

from django.urls import path, include
from . import views
from ajax_select import urls as ajax_select_urls


urlpatterns = [
    path('', views.store, name='store'),
    path('product/filter-data',views.filter_data,name="filter-data"),
    path('category/<slug:category_slug>/', views.store, name='products_by_category'),
    path('sub_category/<slug:sub_category_slug>/', views.store, name='products_by_sub_category'),
    path('main_category/<slug:main_category_slug>/', views.store, name='products_by_main_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('search/', views.search, name='search'),
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
    path('product/ajax_select_urls/',views.filter_sec,name="ajax_select_urls"),


]


