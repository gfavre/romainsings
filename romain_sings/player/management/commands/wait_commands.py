# -*- coding: utf-8 -*-
import os
from django.core.management.base import BaseCommand, CommandError


from ...qrplay import handle_qrcode


def start_scan(process, outstream):
    while True:
        data = process.readline()
        qrcode = str(data)[8:]
        if qrcode:
            outstream.write('Read {}\n'.format(qrcode))
            qrcode = qrcode.rstrip()
            handle_qrcode(qrcode)


class Command(BaseCommand):
    def handle(self, *args, **options):
        p = os.popen('/usr/bin/zbarcam --prescale=300x200 --nodisplay', 'r')
        try:
            self.stdout.write('opening software')
            start_scan(self.stdout)
        except KeyboardInterrupt:
            self.stdout.write('Stopping scanner...')
        finally:
            p.close()
