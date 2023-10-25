from itertools import count
import mysql.connector
from django.http import JsonResponse
from django.template.loader import render_to_string

from .models import Product, ReviewRating, Category

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="ecommerce_website"
)
mycursor = mydb.cursor()

def section_links(request):
    special_offers = Product.objects.filter(section__name_show='special offer')
    for product in special_offers:
        # گرفتن میانگین و تعداد دیدگاه های درج شده برای محصولات
        fetch_reviews = (
            "SELECT AVG(rating) as avgrating, COUNT(rating) as countrating FROM ecommerce_website.store_reviewrating  WHERE "
            "status=1 and product_id=%s;")
        mycursor.execute(fetch_reviews, [product.id])
        reviews_sql = mycursor.fetchall()

        avg = 0
        count = 0
        if reviews_sql is not None:
            product.count_rating = reviews_sql[0][1]
            product.average = reviews_sql[0][0]

    return dict(special_offers=special_offers)



def Avg(product):
        fetch_reviews = (
            "SELECT AVG(rating) as avgrating, COUNT(rating) as countrating FROM ecommerce_website.store_reviewrating  WHERE "
            "status=1 and product_id=%s;")
        mycursor.execute(fetch_reviews, [product.id])
        reviews_sql = mycursor.fetchall()


        if reviews_sql is not None:
            count = reviews_sql[0][1]
            avg = reviews_sql[0][0]
            return avg, count