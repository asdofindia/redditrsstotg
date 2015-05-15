#!/bin/sh

DIR=$1
USER=`whoami`
TGDIR=/home/$USER/$DIR
for f in $(ls downloads); do
  IFS=- read chatid trash <<< $f
  SENDTO="chat#$chatid"
  echo "send_photo $SENDTO $PWD/downloads/$f" | $TGDIR/bin/telegram-cli -W -D -k $TGDIR/server.pub -c $TGDIR/config.sample -p kn
  rm -f "downloads/$f"
done
