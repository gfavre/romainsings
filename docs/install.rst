Install
=========

This is where you write how to get a new laptop to run this project.

APT
---
sudo apt-get install python-dev libpq-dev postgresql postgresql-contrib nginx


Samba
-----

https://www.raspberrypi.org/magpi/samba-file-server/

you *must* have `ntlm auth=yes` in the global section of your smb.conf file in order for SONOS to connect. They are still using an older version of the protocol that newer linux systems have disabled by default.
