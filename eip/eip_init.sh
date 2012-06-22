#!/bin/bash

prog=$(basename $0)
logger="logger -t $prog"

# Wait until networking is up on the EC2 instance.
perl -MIO::Socket::INET -e '
until(new IO::Socket::INET("169.254.169.254:80")){print"Waiting for network...\n";sleep 1}
' | $logger


SCRIPT_DIR=/root
ELASTIC_IP=79.125.7.52

associate_ip() {
    local ACTION=$1
    python ${SCRIPT_DIR}/eip.py ${ELASTIC_IP} $ACTION
}

start() {
  associate_ip start
}

stop() {
  associate_ip stop
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