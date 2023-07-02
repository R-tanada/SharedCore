import threading
from concurrent.futures import ThreadPoolExecutor
import time
import numpy as np


class Task:
    def __init__(self, name) -> None:
        self.name = name
        self._flag = False
        self.cnt = 0

    def t(self):
        if not self._flag:
            self.iter = np.linspace(0, 10, 10)
            self.iter = iter(self.iter)
            self._flag = True
        else:
            try:
                _x = next(self.iter)
                time.sleep(1)
                print(self.name, _x)
            except StopIteration:
                self._flag = False
                print(self.name, "finish")


import copy

if __name__ == "__main__":
    t1 = Task("task1")
    t2 = Task("Task2")
    cnt = 0
    mode = "normal"
    mode = "pool"
    ppp = True
    t1_1 = copy.deepcopy(t1)
    print(t1, t1_1)
    if not ppp:
        while True:
            try:
                cnt += 1
                time.sleep(0.1)
                if mode == "normal":
                    if 3 <= cnt <= 14:
                        t1.t()
                    if 5 <= cnt <= 16:
                        t2.t()
                elif mode == "pool":
                    with ThreadPoolExecutor() as pool:
                        if 3 <= cnt <= 14:
                            pool.submit(t1.t)
                        if 5 <= cnt <= 16:
                            pool.submit(t1_1.t)
            except KeyboardInterrupt:
                break
    else:
        with ThreadPoolExecutor() as pool:
            while True:
                try:
                    cnt += 1
                    time.sleep(0.1)
                    if mode == "normal":
                        pass
                    elif mode == "pool":
                        if 3 <= cnt <= 14:
                            pool.submit(t1.t)
                        if 5 <= cnt <= 16:
                            pool.submit(t1_1.t)
                except KeyboardInterrupt:
                    break
