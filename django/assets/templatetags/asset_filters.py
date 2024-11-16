from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """Multiply the provided value by argument"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0