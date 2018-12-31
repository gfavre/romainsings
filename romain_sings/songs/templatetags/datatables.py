# -*- coding: utf-8 -*-
from django import template


register = template.Library()


LANG_DICT = {'fr': 'fr.json', 'en': 'en.json'}

@register.filter(name='datatable_i18n_url')
def datatable_i18n_url(value):
    """usage: {{ LANGUAGE_CODE | datatable_i18n_url }}"""
    base_lang = value.split('-')[0]
    return LANG_DICT.get(base_lang.lower(), 'en.json')
