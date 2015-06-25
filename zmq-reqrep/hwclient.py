#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import string
import zmq

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

total_recieved = 0
#  Do 26 requests, waiting each time for a response
for request in string.ascii_lowercase:
    #print("Sending request %s ..." % request)
    socket.send_string(request)

    #  Get the reply.
    message = socket.recv()
    total_recieved += len(message)
    #print("Received reply %s [ %s ]" % (request, message))

print("total recieved: {}".format(total_recieved))
