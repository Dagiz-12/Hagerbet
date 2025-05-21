from django import template
from django.template.defaultfilters import floatformat

register = template.Library()


@register.filter
def currency(value):
    try:
        num = float(value)
        return f"${floatformat(num, 2)}"
    except (ValueError, TypeError):
        return value
