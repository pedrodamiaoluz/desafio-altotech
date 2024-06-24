from django.template import Library

register = Library()

@register.filter
def fatiar_lista(lista, quantidade):
    return lista[:quantidade]