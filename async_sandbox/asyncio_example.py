"""
This will show you how async functions are sequenced and how a sync method will block all async
coroutines from continuing. Take note of how the time to complete the async_calc func decreases by ~2s
as the tasks are progressed because the sync_calc function is blocking everything else from continuing
"""

import asyncio
import time

def sync_calc(num) -> int:
    """
    This function will block other functions from running in async because of time.sleep()
    """
    print(f"start sync_calc - input is {num}")

    time.sleep(2)
    output = num **2

    print(f"end sync_calc - output is {output}")
    return output


async def async_calc(num) -> int:
    """
    This function will truly run async
    """
    print(f"start async_calc - input is {num}")

    await asyncio.sleep(2) # change to time.sleep(2) to see it blocking the whole coroutine
    output = num **2

    print(f"end async_calc - output is {output}")
    return output


async def async_example(num) -> str:
    start = time.perf_counter()
    print(f"start async_example - input is {num}")

    output = sync_calc(num)
    post_sync = time.perf_counter()
    output = await async_calc(num)

    end = time.perf_counter()

    print(f"sync_calc total time for input {num} was {post_sync-start}s")
    print(f"async_calc total time for input {num} was {end-post_sync}s")
    print(f"async_example for input {num} - total time was {end-start}s")
    return output


async def main():
    start = time.perf_counter()

    tasks = [async_example(i) for i in range(1,6)]
    await asyncio.gather(*tasks)

    end = time.perf_counter()
    print(f"end main - it took {end-start}s")


if __name__ == "__main__":
    asyncio.run(main())