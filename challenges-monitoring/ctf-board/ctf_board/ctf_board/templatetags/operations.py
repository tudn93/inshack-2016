from django import template
register = template.Library()


@register.filter('multiply')
def multiply(value, arg):
    return value * arg
