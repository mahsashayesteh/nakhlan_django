from django import template
import math

register = template.Library()


@register.simple_tag
def call_sellprice(price, discount):
    if discount is None or discount is 0:

        return price
    else:
        sell_price = price
        sell_price = price - (price * discount / 100)

        return math.floor(sell_price)
