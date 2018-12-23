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
import soco


media_storage = FileSystemStorage(location=str(settings.MEDIA_ROOT), base_url='/uploads/media')
sonos_storage = FileSystemStorage(location=str(settings.SONOS_BASE_DIR), base_url='/uploads/songs')


def upload_to_sonos(instance, filename):
    return os.path.join(slugify(instance.artist), filename)


def qrcode_path(instance, filename):
    return os.path.join(str(instance.uuid), filename)


PLAY_SONG_IMMEDIATELY = 'play'
SMB_PROTOCOL = 'x-file-cifs'


class Song(TimeStampedModel):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255, blank=True)
    illustration = models.ImageField(null=True, blank=True, upload_to=qrcode_path, storage=media_storage)
    qrcode = models.ImageField(null=True, blank=True, upload_to=qrcode_path, storage=media_storage)
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

    @property
    def play_path(self):
        return '{}://{}{}'.format(SMB_PROTOCOL,
                                  settings.SONOS_MOUNT_HOSTNAME,
                                  settings.SONOS_BASE_DIR(str(self.file)))

    def play(self):
        current_device = settings.SONOS_ROOM_NAME
        spkr = soco.discovery.by_name(current_device).group.coordinator
        spkr.play_uri(self.play_path)


# TODO: modèle de statistiques de lecture
# TODO: carte album?

