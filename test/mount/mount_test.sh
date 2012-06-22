#!/bin/bash

declare -a DEVICES
declare -a MOUNTPOINTS

DEVICES=("dev1" "dev2")
MOUNTPOINTS=("mnt1" "mnt2")


exec() {
    local ACTION=$1
    python ../../mount/mount.py ${DEVICES[@]} ${MOUNTPOINTS[@]} $ACTION
}

start() {
    exec mount
}

stop() {
    exec unmount
}


case "$1" in
    start)
        start
        ;;

    stop)
        stop
        ;;
    restart)
        stop
        sleep 5
        start
        ;;
    *)
        echo "Usage: $SELF {start|stop|restart}"
        exit 1
        ;;
esac

exit 0