from django import template

register = template.Library()

@register.filter
def get(dictionary, key):
    return dictionary[key]

@register.filter
def centsToStr(cents: int) -> str:
    actualCents = cents % 100
    price = str(cents // 100)
    if actualCents != 0:
        if actualCents < 10:
            actualCents = str(actualCents) + "0"
        price = "{}.{}".format(price, actualCents)
    return price
