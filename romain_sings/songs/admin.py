# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from .models import Song


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'created', 'illustration_tag')

    def illustration_tag(self, obj):
        if obj.illustration:
            return format_html('<img src="{}" style="max-height: 45px; max-width:45px;"/>'.format(obj.illustration.url))
        return ''
    illustration_tag.short_description = _("Illustration")


