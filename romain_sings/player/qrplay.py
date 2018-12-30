# -*- coding: utf-8 -*-
from django.conf import settings

import soco

from romain_sings.songs.models import Song, PLAY_SONG_IMMEDIATELY
from .models import PlayedEvent


SMB_PROTOCOL = 'x-file-cifs'

player = soco.discovery.by_name(settings.SONOS_ROOM_NAME).group.coordinator


def play(qr_id):
    try:
        value = hex(int(qr_id)).split('x')[-1]
    except:
        return
    try:
        song = Song.objects.filter(uuid__startswith=value).first()
        PlayedEvent.objects.create(song=song)
        player.play_uri(song.play_path)
    except AttributeError:
        return


def stop():
    player.stop()


def handle_qrcode(qrcode):
    command, *arguments = qrcode.split(':')
    if command == PLAY_SONG_IMMEDIATELY:
        play(arguments[0])
    elif command == 'stop':
        stop()
