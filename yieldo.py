import heapq
import time
from collections import deque


class Scheduler:
    def __init__(self):
        self.ready = deque()
        self.current = None
        self.sleeping = []
        self.sequence = 0

    def add_new_task(self, gen):
        self.ready.append(gen)

    async def sleep(self, delay):
        deadline = time.time() + delay
        heapq.heappush(self.sleeping, (deadline, self.sequence, self.current))
        self.sequence += 1
        self.current = None
        await switch()


    def run(self):
        while self.ready or self.sleeping:
            if not self.ready:
                deadline, _, coro = heapq.heappop(self.sleeping)
                delta = deadline - time.time()
                if delta > 0:
                    time.sleep(delta)
                self.ready.append(coro)
            self.current = self.ready.popleft()
            try:
                if self.current is None:
                    continue
                self.current.send(None)
                self.ready.append(self.current)
            except StopIteration:
                pass

class Awaitable():
    def __init__(self):
        pass
    def __await__(self):
        yield

def switch():
    return Awaitable()

async def countup(stop):
    n = 0
    while n < stop:
        print("Up: ", n)
        await sched.sleep(4)
        n += 1

async def countdown(n):
    while n > 0:
        print("Down: ", n)
        await sched.sleep(1)
        n -= 1


sched = Scheduler()
sched.add_new_task(countup(5))
sched.add_new_task(countdown(20))
sched.run()