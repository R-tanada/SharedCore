import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import psutil


def func(*args):
    global flag
    global pos

    pos += 1
    print("Start", args, pos)
    time.sleep(0.01)

    if args[0] == 0:
        pos += 10
    elif args[0] == 1:
        pos -= 10

    print("End", args, pos)

    # if args[0] == 1000:
    #     print(time.time() - start_time)
    #     flag = True


def pool():
    with ThreadPoolExecutor() as pool:
        for i in range(2):
            pool.submit(func, i)


def thr():
    for i in range(2):
        th = threading.Thread(target=func, args=(i), daemon=True)
        th.start()


if __name__ == "__main__":
    pos = 0
    flag = False
    start_time = time.time()
    while True:
        try:
            pool()
            print(pos)
            # thr()

            if flag:
                break

        except KeyboardInterrupt:
            break
