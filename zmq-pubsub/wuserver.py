#
#   PUB-SUB server
#   Binds PUB socket to tcp://*:5556
#

import random
import string
import zmq

message = random.choice(string.ascii_lowercase) * 1024

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5556")

while True:
    socket.send_string(message)
