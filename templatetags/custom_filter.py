from django import template
import random
register=template.Library()

@register.filter(name="add_rupee")
def add_rupee(number):
    return '₹ '+str(number)

@register.filter(name="discount_price")
def discount_price(number1,number2):
    return (number1-(number1*number2)/100);

@register.filter(name="sale_price")
def sale_rupee(product):
    return (product.price-(product.price*product.discount)/100);
