from django import template

register = template.Library()


@register.filter
def mult(quantity, price):
    return str(quantity * price).replace(',', '.')
