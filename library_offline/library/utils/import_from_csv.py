import asyncio

import aiofiles
from aiocsv import AsyncReader


async def reading_csv(file_name) -> list:
    async with aiofiles.open(f"library/upload/{file_name}", mode="r", encoding="utf-8", newline="") as afp:
        data: list = [row async for row in AsyncReader(afp)]
    return data


def run_reading_csv(file_name):
    return(asyncio.run(reading_csv(file_name)))