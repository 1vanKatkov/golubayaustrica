from decimal import Decimal, InvalidOperation

from django import template

register = template.Library()


def _normalize_decimal(value):
    if value is None:
        return None
    if isinstance(value, Decimal):
        return value
    try:
        return Decimal(value)
    except InvalidOperation:
        return None


@register.filter
def format_result(value):
    """Show integer when there is no fractional part; otherwise use comma decimal."""

    val = _normalize_decimal(value)
    if val is None:
        return ""

    if val == val.to_integral():
        return str(val.to_integral())

    normalized = val.normalize()
    text = format(normalized, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text.replace(".", ",")


@register.filter
def has_positive(value):
    val = _normalize_decimal(value)
    return val is not None and val > 0


@register.filter
def has_negative(value):
    val = _normalize_decimal(value)
    return val is not None and val < 0


@register.filter
def format_with_sign(value):
    val = _normalize_decimal(value)
    if val is None:
        return ""
    formatted = format_result(val)
    if val > 0:
        return "+" + formatted
    return formatted

