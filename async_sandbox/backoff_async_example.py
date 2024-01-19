"""
This shows the behaviour of the backoff decorator on a function you might want to retry several 
times e.g an api call. This uses on_predicate to show the behaviour with a simple predicate but 
typically you would use on_exception to catch specific api errors.
"""
import asyncio
import backoff
import time

def backoff_handler(details):
    print ("Backing off {wait:0.1f} seconds after {tries} tries "
           "calling function {target} with args {args} and kwargs "
           "{kwargs}".format(**details))

@backoff.on_predicate(backoff.expo, lambda x: x < 2, max_tries=5, on_backoff=backoff_handler)
async def async_backoff(num):
    print(f"start async_backoff - input is {num}")
    output = num**2
    print(f"end async_backoff - output is {output}")
    return output

async def async_example(num):
    start = time.perf_counter()
    print(f"start async_example - input is {num}")

    result = await async_backoff(num)

    end = time.perf_counter()
    print(f"end async_example - output is {result} - total time was {end-start}s")


async def main():
    tasks = [async_example(i) for i in range(1,3)]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())