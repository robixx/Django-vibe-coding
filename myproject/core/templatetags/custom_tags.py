from django import template

register = template.Library()

@register.filter
def dict_key(d, k):
    """Access a dictionary by key."""
    return d.get(k)
