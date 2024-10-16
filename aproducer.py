# Producer-Consumer without using thread.

from collections import deque
import time
import heapq


class Scheduler:
    def __init__(self):
        self.current = deque()
        self.sleeping = []
        self.sequence = 0

    def run(self):
        while self.current or self.sleeping:
            if not self.current:
                delay, _, func = heapq.heappop(self.sleeping)
                delta = delay - time.time()
                if delta > 0:
                    time.sleep(delta)
                self.current.append(func)
            while self.current:
                func = self.current.popleft()
                func()

    def add(self, delay, func):
        run_at = time.time() + delay
        heapq.heappush(self.sleeping, (run_at, self.sequence, func))
        self.sequence += 1


class QueueClosed(Exception):
    def __init__(self):
        pass

class AsyncQueue(object):
    def __init__(self):
        self.items = deque()
        self.waiting = deque()
        self._close = False

    def put(self, n):
        if self._close:
            raise QueueClosed()
        self.items.append(n)
        if self.waiting:
            func = self.waiting.popleft()
            sched.add(0, func)


    def get(self):
        if self.items:
            return self.items.popleft()
        else:
            if self._close:
                raise QueueClosed()
            else:
                self.waiting.append(self.get)

    def close(self):
        self._close = True


def producer(n):
    if n == 0:
        q.close()
        print("Done Producing")
        return
    print("Producing ", n)
    q.put(n)
    sched.add(1, lambda : producer(n - 1))


def consumer():
    try:
        n = q.get()
    except QueueClosed:
        print("Done consuming")
        return
    print("Consuming ", n)
    sched.add(1, consumer)

q = AsyncQueue()
sched = Scheduler()
sched.add(0, lambda : producer(10))
sched.add(0, consumer)
sched.run()