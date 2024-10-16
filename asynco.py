import time
import heapq
from collections import deque


class Scheduler:
    def __init__(self):
        self.q = deque()
        self.sleeping = []
        self.sequence = 0

    def run(self):
        while self.q or self.sleeping:
            if not self.q:
                delay, _, func = heapq.heappop(self.sleeping)
                delta = delay - time.time()
                if delta > 0:
                    time.sleep(delta)
                self.q.append(func)
            while self.q:
                func = self.q.popleft()
                func()

    def add(self, delay, func):
        run_at = time.time() + delay
        heapq.heappush(self.sleeping, (run_at, self.sequence, func))
        self.sequence += 1

def countup(stop):
    x = 0
    def _run():
        nonlocal x
        if x == stop:
            return
        print("Up: ", x)
        x += 1
        sched.add(4, lambda : _run())
    _run()

def countdown(start):
    if start == 0:
        return
    print("down", start)
    sched.add(1, lambda : countdown(start - 1))


sched = Scheduler()
sched.add(0, lambda : countup(5))
sched.add(0, lambda : countdown(20))
sched.run()
