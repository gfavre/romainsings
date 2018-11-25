# -*- coding: utf-8 -*-
import os
import uuid

from django.db import models
from django.conf import settings
from django.utils.text import slugify

from model_utils.models import TimeStampedModel


def upload_to_sonos(instance, filename):
    # TODO cvompleter pour que ça sauve dans le dossier partagé de sonos, selon le classement prévu.
    return os.path.join(settings.SONOS_BASE_DIR, slugify(instance.artist), filename)


class Song(TimeStampedModel):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255, blank=True)
    illustration = models.ImageField(null=True, blank=True)
    qrcode = models.ImageField(null=True, blank=True)
    file = models.FileField(null=True, upload_to=upload_to_sonos)

    @property
    def qr_id(self):
        return str(self.uuid.fields[0])

    def __str__(self):
        return '{}: {}'.format(self.artist, self.title)

    # todo: method de génération du qrcode

    # TODO: extraction des données depuis la chanson


# TODO: modèle de statistiques de lecture
# TODO: carte album?

