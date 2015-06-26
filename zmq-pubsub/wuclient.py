#
#   PUB_SUB client
#   Connects SUB socket to tcp://localhost:5556
#

import sys
import zmq

DATA_UNIT = 1024 * 1024

#  Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

print("Collecting updates from server...")
socket.connect("tcp://localhost:5556")

socket.setsockopt_string(zmq.SUBSCRIBE, '')

# Process 5 updates
total_temp = 0
while True:
    string = socket.recv_string()
    total_temp += len(string)
    if total_temp > DATA_UNIT * 10:
        break

print("Total reveived: {}".format(total_temp))
