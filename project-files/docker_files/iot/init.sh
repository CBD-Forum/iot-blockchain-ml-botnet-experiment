#!/bin/bash

# mirai prefers busybox telnetd
cd /root
touch .hushlogin
wget https://www.busybox.net/downloads/binaries/1.26.2-i686/busybox 2>/dev/null
chmod +x busybox
cp busybox /bin

tmux new-session -d -s telnetd "./busybox telnetd -F"

/usr/bin/supervisord -c /etc/supervisord.conf
