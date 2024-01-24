"""
This example is using asyncio & backoff to call the OpenAI chat completion API.

For testing, it handles the case when you're trying to connect to OpenAI but you have no network 
and therefore receive an APIConnectionError, which should of course be replaced with something else like a
RateLimitError in production usage.
"""
import asyncio
import backoff
import openai
import os
import time

client = openai.AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def backoff_handler(details):
    print(
        "Backing off {wait:0.1f} seconds after {tries} tries "
        "calling function {target} with args {args} and kwargs "
        "{kwargs}".format(**details)
    )


def backoff_gen():
    num = 2
    while True:
        yield num
        num += num * 2


@backoff.on_exception(
    backoff_gen,
    (openai.APIConnectionError, openai.RateLimitError),
    max_tries=3,
    on_backoff=backoff_handler,
    jitter=None,
)
async def call_api(num):
    print(f"Calling API for input: {num}")
    chat_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"What is {num} squared?",
            }
        ],
        model="gpt-3.5-turbo",
        max_tokens=10,
    )

    await asyncio.sleep(1)
    response = chat_completion.choices[0].message.content
    print(response)

    return response

def batch_tasks(tasks, batch_size):
    for i in range(0, len(tasks), batch_size):  
        yield tasks[i:i + batch_size] 


async def main():

    loop_count = 1

    # OpenAI throttled when sending a batch of more than 100 requests at once
    batch_size = 5

    tasks = [call_api(i) for i in range(0, 10)]
    print(f"Batching requests for {len(tasks)} tasks")

    print(batch_tasks(tasks, batch_size))

    for batch in batch_tasks(tasks, batch_size):
        start = time.perf_counter()

        print(f"Calling API for batch {loop_count} with {len(batch)} tasks")
        await asyncio.gather(*batch)

        end = time.perf_counter()

        print(f"Finished batch {loop_count} in {'{0:2f}'.format(end-start)}s")

        loop_count += 1


if __name__ == "__main__":
    asyncio.run(main())
