from concurrent.futures import ThreadPoolExecutor
import time


def f(n):
    print("start", n)
    time.sleep(1)
    print("end", n)


cnt = 0

while True:
    cnt += 1
    time.sleep(1)
    try:
        with ThreadPoolExecutor(max_workers=2) as pool:
            for i in range(2):
                pool.submit(f, cnt)
    except KeyboardInterrupt:
        break
