#
#   PUB-SUB server
#   Binds PUB socket to tcp://*:5556
#

import sys
import random
import string
import zmq

multiple = int(sys.argv[1]) if len(sys.argv) > 1 else 1
message = random.choice(string.ascii_lowercase) * 1024 * 1

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5556")

while True:
    socket.send_string(message)
