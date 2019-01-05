from django.db import models

from model_utils.models import TimeStampedModel


class PlayedEvent(TimeStampedModel):
    song = models.ForeignKey('songs.Song', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ('created',)
