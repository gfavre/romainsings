# -*- coding: utf-8 -*-
from io import BytesIO
import os
import uuid

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils.text import slugify

from model_utils.models import TimeStampedModel
import qrcode


sonos_storage = FileSystemStorage(location=settings.SONOS_BASE_DIR, base_url='/uploads')


def upload_to_sonos(instance, filename):
    return os.path.join(slugify(instance.artist), filename)


def qrcode_path(instance, filename):
    return os.path.join(str(instance.uuid), filename)


PLAY_SONG_IMMEDIATELY = 'play'


class Song(TimeStampedModel):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255, blank=True)
    illustration = models.ImageField(null=True, blank=True)
    qrcode = models.ImageField(null=True, blank=True, upload_to=qrcode_path)
    file = models.FileField(null=True, upload_to=upload_to_sonos, storage=sonos_storage)

    @property
    def qr_id(self):
        return str(self.uuid.fields[0])

    def __str__(self):
        return '{}: {}'.format(self.artist, self.title)

    def build_qr(self, commit=True):
        img = qrcode.make('{}:{}'.format(PLAY_SONG_IMMEDIATELY, self.qr_id))
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        file_content = ContentFile(buffer.getvalue())
        self.qrcode.save('qrcode.png', file_content)
        if commit:
            self.save()

    def save(self, *args, **kwargs):
        if not self.qrcode:
            self.build_qr(commit=False)
        super().save(*args, **kwargs)


# TODO: modèle de statistiques de lecture
# TODO: carte album?

