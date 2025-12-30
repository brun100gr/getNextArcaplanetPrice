#!/bin/bash

# Imposta timezone
ln -sf /usr/share/zoneinfo/Europe/Rome /etc/localtime
echo "Europe/Rome" > /etc/timezone

# Avvia SSH
/usr/sbin/sshd -D
