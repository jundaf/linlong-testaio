#
#   Usage:
#       mtclient.py
#       mtclient.py SERVER_NAME
#       mtclient.py SERVER_NAME DATA_SIZE
#       mtclient.py SERVER_NAME DATA_SIZE PROCESSES THREADS
#

import sys
import os
import string
import time
import threading
import queue
import functools
import multiprocessing as mp
import zmq


PROCESS_NUM = 10
WORKER_NUM = 10
DATA_UNIT = 1024 * 1024
DATA_SIZE = 100


def gen_request():
    while True:
        for req in string.ascii_lowercase:
            yield req


def worker_routine(que, server, units):
    context = zmq.Context().instance()
    #~ print("{} {}".format(context.get(zmq.IO_THREADS),
                         #~ context.get(zmq.MAX_SOCKETS)))

    socket = context.socket(zmq.REQ)
    socket.connect("tcp://{}:5555".format(server))

    total_recieved = 0
    begin_time = time.time()
    for request in gen_request():
        socket.send_string(request)
        message = socket.recv()

        total_recieved += len(message)
        if total_recieved > DATA_UNIT * units:
            break

    elapsed = time.time() - begin_time
    #self = threading.current_thread()
    #print("{} recieved {} in {}".format(self.name, total_recieved, elapsed))
    que.put(elapsed)
    socket.close()


def mainf(task_id):
    q = queue.Queue()
    for i in range(WORKER_NUM):
        thread = threading.Thread(target=worker_routine, args=(q, server, units))
        thread.start()

    results = []
    for i in range(WORKER_NUM):
        results.append(q.get())

    total = functools.reduce(lambda x, y: x + y, results)
    average = total / WORKER_NUM
    #print("[{}] average time: {}".format(os.getpid(), average))
    return average


if __name__ == '__main__':
    server = 'localhost'
    units = DATA_SIZE # default to 100M
    if len(sys.argv) >= 2:
        server = sys.argv[1]
    if len(sys.argv) >= 3:
        units = int(sys.argv[2])
    print("Server: {} \nUnits: {}m".format(server, units))

    if len(sys.argv) >= 4:
        PROCESS_NUM = int(sys.argv[3])
    if len(sys.argv) >= 5:
        WORKER_NUM = int(sys.argv[4])
    print("Connections: {}".format(PROCESS_NUM * WORKER_NUM))

    with mp.Pool(PROCESS_NUM) as pool:
        elapsed = pool.map(mainf, range(PROCESS_NUM))
        total = functools.reduce(lambda x, y: x + y, elapsed)
        print("Average time {:.2f}s".format(total / PROCESS_NUM))
