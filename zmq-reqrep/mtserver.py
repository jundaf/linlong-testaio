"""

   Multithreaded Reqrep server

   Author: Guillaume Aubert (gaubert) <guillaume(dot)aubert(at)gmail(dot)com>

   Author: Junda Feng

"""
import time
import threading
import zmq

WORKER_NUM = 5
DEFAULT_SIZE = 1024

BUFFERS = {}


def setup_buffers():
    """Prepare responses"""

    import sys, string
    buffer_size = DEFAULT_SIZE
    if len(sys.argv) >= 2:
        buffer_size = int(sys.argv[1])

    print("Set buffer size to {}".format(buffer_size))

    for letter in string.ascii_lowercase:
        BUFFERS[letter] = letter * buffer_size


def worker_routine(worker_url, context=None):
    """Worker routine"""

    context = context or zmq.Context.instance()
    # Socket to talk to dispatcher
    socket = context.socket(zmq.REP)
    socket.connect(worker_url)

    while True:
        try:
            request = socket.recv_string()
            #send reply back to client
            socket.send_string(BUFFERS[request])
        except zmq.ContextTerminated:
            break

def main():
    """Server routine"""

    url_worker = "inproc://workers"
    url_client = "tcp://*:5555"

    setup_buffers()

    # Prepare our context and sockets
    context = zmq.Context.instance()

    # Socket to talk to clients
    clients = context.socket(zmq.ROUTER)
    clients.bind(url_client)

    # Socket to talk to workers
    workers = context.socket(zmq.DEALER)
    workers.bind(url_worker)

    # Launch pool of worker threads
    for i in range(WORKER_NUM):
        thread = threading.Thread(target=worker_routine, args=(url_worker,))
        thread.start()

    try:
        zmq.device(zmq.QUEUE, clients, workers)
    except KeyboardInterrupt:
        pass

    # We never get here but clean up anyhow
    clients.close()
    workers.close()
    context.term()


if __name__ == "__main__":
    main()
