#!/bin/bash

APPNAME=$1;
VULNERABLE_IOT_OBJECTS=$2;

APP_NUMBER=$(echo $APPNAME | grep -o -E '[0-9]+')

if (( $APP_NUMBER < $VULNERABLE_IOT_OBJECTS )); then
# set root password
passwd root << EOF
root
root
EOF

# enable remote root shell
cat >> /etc/securetty << EOF
pts/0
pts/1
pts/2
pts/3
pts/4
pts/5
pts/6
pts/7
pts/8
pts/9
EOF
fi
