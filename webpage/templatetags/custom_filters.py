from django import template

register = template.Library()

@register.filter(name='formato_cl')
def formato_chileno(valor):
    if isinstance(valor, int):
        return f"{valor:,}".replace(",", ".")
    return valor