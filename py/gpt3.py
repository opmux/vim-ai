#!/usr/bin/env python
"""
https://github.com/Ruu3f/freeGPT/blob/main/freeGPT/AsyncClient/gpt3.py
freeGPT's gpt3 async client with stream support
"""
from aiohttp import ClientSession, ClientError
import asyncio
import sys

async def gpt3(prompt):
    async with ClientSession() as session:
        try:
            async with session.post(
                url="https://api.binjie.fun/api/generateStream",
                headers={
                    "origin": "https://chat.jinshutuan.com",
                    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36",
                },
                json={
                    "prompt": prompt,
                    # "system": "Rependre toujours en Français.",
                    "system": "Always talk in English.",
                    "withoutContext": False,
                    "stream": True,
                },
            ) as resp:
                async for byte in resp.content.iter_chunked(2400):
                    yield byte.decode('utf-8')
                    # print(f"{byte.decode('utf-8')}", end="")
        except ClientError as exc:
            raise ClientError("Unable to fetch the response.") from exc

async def loop_chat():
    while True:
        prompt = input(">>> ")
        async for r in gpt3(prompt):
            print(f"{r}", end="")
        print("\n")

async def complete():
    prompt = sys.argv[1]
    async for r in gpt3(prompt):
        print(f"{r}", end="")

if len(sys.argv) > 1:
    asyncio.run(complete())
else:
    asyncio.run(loop_chat())
