from django import template

register = template.Library()


@register.filter
def mult(quantity, price):
    return quantity * price
