from django import template
register = template.Library()


@register.filter('access')
def access(dictionnary, index):
    return dictionnary[index]
