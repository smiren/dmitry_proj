from django import template
from decimal import Decimal
import string

register = template.Library()


@register.simple_tag(takes_context=True)
def menu_highlight(context, url, group_url=False):
    """Тег для подсветки текущего активного элемента меню."""
    path = context['request'].get_full_path()
    result = url in path if group_url else url == path
    return 'active' if result else ''


@register.filter
def phone(value):
    """Фильтр для отображения номера телефона."""
    if not list(filter(lambda x: x in string.digits, value)) or len(value) != 10:
        return value
    return f"+7 ({value[:3]}) {value[3:6]}-{value[6:8]}-{value[8:]}"


@register.filter
def price_pos(value, quantity=1):
    return f"{Decimal(value)*quantity:.2f}"


@register.filter
def addstr(val1, val2):
    return f"{val1}{val2}"
