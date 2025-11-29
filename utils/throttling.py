import asyncio
from collections import defaultdict
from time import time

class Throttler:
    def __init__(self, rate=1, per=1.0):
        self.rate = rate
        self.per = per
        self.calls = defaultdict(list)

    async def throttle(self, key):
        now = time()
        q = self.calls[key]
        q = [t for t in q if t > now - self.per]
        if len(q) >= self.rate:
            await asyncio.sleep(self.per - (now - q[0]))
        q.append(time())
        self.calls[key] = q
