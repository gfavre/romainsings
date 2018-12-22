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



def handle(self, *args, **options):
    p = os.popen('/usr/bin/zbarcam --prescale=300x200', 'r')
    try:
        start_scan(p)
    except KeyboardInterrupt:
        print('Stopping scanner...')
    finally:
        p.close()
