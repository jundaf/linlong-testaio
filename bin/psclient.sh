#!/bin/bash

SERVER=172.16.0.158
WUCLIENT=zmq-pubsub/wuclient.py

if [ -f "$WUCLIENT" ]; then
    CLIENT="$WUCLIENT"
else
    CLIENT="../$WUCLIENT"
fi

python3 $CLIENT $SERVER $*
