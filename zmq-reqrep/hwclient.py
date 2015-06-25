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

total_received = 0
#  Do 10 requests, waiting each time for a response
for request in string.ascii_lowercase[:10]:
    print("Sending request %s ..." % request)
    socket.send_string(request)

    #  Get the reply.
    message = socket.recv_string()
    total_received += len(message)
    print("Received reply %s [ %s ]" % (request, len(message)))

print("Total received {}".format(total_received))
