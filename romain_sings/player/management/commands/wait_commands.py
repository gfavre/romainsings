# -*- coding: utf-8 -*-
import os
from django.core.management.base import BaseCommand, CommandError


from ...qrplay import handle_qrcode


def start_scan(process):
    while True:
        data = process.readline()
        qrcode = str(data)[8:]
        if qrcode:
            qrcode = qrcode.rstrip()
            handle_qrcode(qrcode)


class Command(BaseCommand):
    def handle(self, *args, **options):
        p = os.popen('/usr/bin/zbarcam --prescale=300x200', 'r')
        try:
            self.stdout.write('opening software')
            start_scan(p)
        except KeyboardInterrupt:
            self.stdout.write('Stopping scanner...')
        finally:
            p.close()
