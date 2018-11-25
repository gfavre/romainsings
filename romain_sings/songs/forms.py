# -*- coding: utf-8 -*-
import binascii

from django import forms
from django.core.files.base import ContentFile

import mutagen

from .models import Song


class SongUploadForm(forms.ModelForm):

    class Meta:
        model = Song
        fields = ['file']

    def save(self, *args, **kwargs):
        file = self.cleaned_data['file']
        mfile = mutagen.File(file)

        if '©nam' in mfile:
            # mp4
            self.instance.title = mfile['©nam'][0]
            if '©ART' in mfile:
                self.instance.artist = mfile['©ART'][0]
            if 'covr' in mfile:
                mutagen_cover = mfile['covr'][0]
                if mutagen_cover.imageformat == mutagen_cover.FORMAT_JPEG:
                    extension = 'jpg'
                else:
                    extension = 'png'
                # mutagen_cover.hex returns hexadecimal represented as a string (!) e.g. 'af123b'
                file_content = ContentFile(binascii.unhexlify(mutagen_cover.hex()))
                self.instance.illustration.save('cover.{}'.format(extension), file_content)
        elif 'TIT2' in mfile:
            # mp3
            self.instance.title = mfile['TIT2'].text[0]
            if 'TPE1' in mfile:
                self.instance.artist = mfile['TPE1'][0]
            if 'APIC:' in mfile:
                # APIC files are jpeg stored as binary value.
                file_content = ContentFile(mfile['APIC:'].data)
                self.instance.illustration.save('cover.jpg', file_content)

        return super().save(*args, **kwargs)
