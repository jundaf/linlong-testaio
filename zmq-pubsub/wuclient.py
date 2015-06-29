#
#   PUB_SUB client
#   Connects SUB socket to tcp://localhost:5556
#

import os
import sys
import time
import functools
import threading
import queue
import multiprocessing as mp
import zmq

PROCESS_NUM = 10
WORKER_NUM = 10
DATA_UNIT = 1024 * 1024
DATA_SIZE = 100


def worker_routine(que):
    #  Socket to talk to server
    context = zmq.Context().instance()
    socket = context.socket(zmq.SUB)

    # print("Collecting updates from server...")
    socket.connect("tcp://{}:5556".format(server))

    socket.setsockopt_string(zmq.SUBSCRIBE, '')

    begin_time = time.time()
    total_temp = 0
    while True:
        string = socket.recv_string()
        total_temp += len(string)
        if total_temp > DATA_UNIT * units:
            break

    elapsed = time.time() - begin_time
    que.put(elapsed)
    #print("Total reveived: {} in {}".format(total_temp, elapsed))
    socket.close()


def start_workers(task_id):
    q = queue.Queue()
    for i in range(WORKER_NUM):
        thread = threading.Thread(target=worker_routine, args=(q,))
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
        elapsed = pool.map(start_workers, range(PROCESS_NUM))
        total = functools.reduce(lambda x, y: x + y, elapsed)
        print("Average time {:.2f}s".format(total / PROCESS_NUM))
