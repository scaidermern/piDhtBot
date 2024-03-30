#!/bin/sh
#
# automatic restart on error
#

cd "$(dirname "$0")"

while true; do
    ./piDhtBot.py
    sleep 0.2
    killall libgpiod_pulsein
    sleep 0.2
    killall -9 libgpiod_pulsein
    echo "Restarting..."
done
