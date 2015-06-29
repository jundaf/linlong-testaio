#!/bin/bash

SERVER=172.16.0.158
MTCLIENT=zmq-reqrep/mtclient.py

if [ -f "$MTCLIENT" ]; then
    CLIENT="$MTCLIENT"
else
    CLIENT="../$MTCLIENT"
fi

python3 $CLIENT $SERVER $*
