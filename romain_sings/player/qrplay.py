# -*- coding: utf-8 -*-
from django.conf import settings

import soco

from romain_sings.songs.models import Song, PLAY_SONG_IMMEDIATELY

SMB_PROTOCOL = 'x-file-cifs'

player = soco.discovery.by_name(settings.SONOS_ROOM_NAME).group.coordinator




def play(qr_id):
    song = Song.objects.filter(uuid__startswith=qr_id).first()
    player.play_uri(song.play_path)


def stop():
    player.stop()


def handle_qrcode(qrcode):
    command, *arguments = qrcode.split(':')
    if command == PLAY_SONG_IMMEDIATELY:
        play(arguments[0])
    elif command == 'stop':
        stop()
