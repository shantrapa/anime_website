from django import template
from anime.models import *

register = template.Library()

@register.filter
def get_item_by_id(queryset, id):
    return queryset.filter(id=id).first()

@register.filter
def translate_sort_by(sort_by):
    translations = {
        'rating': 'Рейтингу',
        'release_date': 'Дате Релиза',
        'title': 'Названию',
        'episodes': 'Эпизодам',
    }
    return translations.get(sort_by, sort_by)