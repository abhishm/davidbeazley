import asyncio

async def countup(stop):
    n = 0
    while n < stop:
        print("Up: ", n)
        await asyncio.sleep(4)
        n += 1

async def countdown(n):
    while n > 0:
        print("Down: ", n)
        await asyncio.sleep(1)
        n -= 1

async def main():
    await asyncio.gather(countup(5), countdown(20))

asyncio.run(main())