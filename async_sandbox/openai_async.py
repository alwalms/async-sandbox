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


async def main():
    tasks = [call_api(i) for i in range(0, 3)]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
