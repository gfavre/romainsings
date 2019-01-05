from django.contrib import admin

from .models import PlayedEvent


@admin.register(PlayedEvent)
class PlayedEventAdmin(admin.ModelAdmin):
    list_display = ('song', 'created')
