import queue
import threading
import time

def producer(q, n):
    while n > 0:
        print("Producing ", n)
        q.put(n)
        n -= 1
        time.sleep(1)
    q.put(None)
    print("Done Producing")

def consumer(q):
    while True:
        n = q.get()
        if not n:
            break
        print("Consuming ", n)
        time.sleep(1)
    print("Done consuming")

# A thread safe queue
q = queue.Queue()
p = threading.Thread(target=producer, args=(q, 10)).start()
c = threading.Thread(target=consumer, args=(q,)).start()