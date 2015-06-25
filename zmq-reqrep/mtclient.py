#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import time
import threading
import queue
import functools
import multiprocessing as mp
import os
import zmq


PROCESS_NUM = 4
WORKER_NUM = 10
DATA_UNIT = 1024 * 1024


def gen_request():
    import string
    while True:
        for req in string.ascii_lowercase:
            yield req


def worker_routine(que):
    self = threading.current_thread()
    context = zmq.Context().instance()
    #~ print("{} {}".format(context.get(zmq.IO_THREADS),
                         #~ context.get(zmq.MAX_SOCKETS)))

    #print("{} connecting to server...".format(self.name))
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    total_recieved = 0
    begin_time = time.time()
    for request in gen_request():
        socket.send_string(request)
        message = socket.recv()

        total_recieved += len(message)
        if total_recieved > DATA_UNIT * 10:
            break

    elapsed = time.time() - begin_time
    #print("{} recieved {} in {}".format(self.name, total_recieved, elapsed))
    que.put(elapsed)
    socket.close()


def mainf(task_id):
    q = queue.Queue()
    for i in range(WORKER_NUM):
        thread = threading.Thread(target=worker_routine, args=(q,))
        thread.start()
    results = []
    for i in range(WORKER_NUM):
        results.append(q.get())
    total = functools.reduce(lambda x, y: x + y, results)
    average = total / WORKER_NUM
    print("[{}] average time: {}".format(os.getpid(), average))
    return average


if __name__ == '__main__':
    with mp.Pool(PROCESS_NUM) as pool:
        pool.map(mainf, range(PROCESS_NUM))