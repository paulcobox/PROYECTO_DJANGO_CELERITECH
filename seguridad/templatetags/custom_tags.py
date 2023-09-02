from django import template
from seguridad.models import Privilegio
register = template.Library()


# @register.filter
# def view(value, arg):
#     privilegio = Privilegio.objects.filter(perfil__id=arg,menuitem__id=value).first()
#     return privilegio.view

@register.filter
def check_unchecked_icon(value):
    if value == '1':
        return 'fa-check text-success'
    return 'fa-times text-danger'

@register.filter
def get_checked_by_value(value):
    print(value)
    if value == '1':
        return 'checked'
    return ''

@register.filter
def show_accordion(value):
    print('show:', value)
    if value == 1:
        return 'show'
    return ''

@register.filter
def desc(value):
    print(value)
    if value == '001':
        return 'Activado'
    if value == '002':
        return 'Desactivado'
    if value == '003':
        return 'Eliminado'
    return ''


@register.filter
def get_num_registro(value,num_pagina):
    result = value + (num_pagina-1)*5
    return result

# @register.simple_tag
# def call_method(obj, method_name, *args):
#     method = getattr(obj, method_name)
#     return method(*args)

@register.simple_tag
def get_privilegio_menuitem(menuitem_id,perfil_id):
    # print('entro')
    privilegio = Privilegio.objects.filter(perfil__id=perfil_id,menuitem__id=menuitem_id).first()
    return privilegio