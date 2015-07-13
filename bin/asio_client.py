#!/usr/bin/env python3

import logging
import subprocess
import threading
import queue
import os.path
from functools import reduce

WORKER_NUM = 2
EXEC = 'echo_client'
HOST = 'localhost'
PORT = '5555'

def worker_thread(qq, exe):
    ""
    try:
        qq.put(subprocess.check_output([exe, HOST, PORT]))
    except Exception as e:
        logging.exception("")

def main():
    ""
    dir_ = os.path.dirname(__file__)
    exe = os.path.join(dir_, EXEC)
    logging.info("%s running", exe)
    qq = queue.Queue()
    workers = (threading.Thread(target=worker_thread, args=(qq, exe))
               for i in range(WORKER_NUM))
    for w in workers:
        w.start()
    duration = []
    for i in range(WORKER_NUM):
        t = qq.get().decode()
        duration.append(int(t.split()[0]))
    total = reduce(lambda x,y: x + y, duration)
    logging.info("%d ms", total // WORKER_NUM)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
