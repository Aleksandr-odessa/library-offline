import asyncio
from typing import Any
from random import choice, randint

import aiofiles
from aiocsv import AsyncWriter
from faker import Faker
from library_offline.library.utils.data import AVAILABILITY
fake = Faker("ru_RU")


def create_fake_readers() -> list:
    fake_data = []
    for _ in range(5):
        fake_address: list = fake.address().split(",")
        address: str = f'г. Москва {" ".join(fake_address[1:3])}'
        fake_data.append([fake.name(), address, fake.ascii_email()])
    return fake_data


def create_fake_books() -> list:
    fake_data = []
    for _ in range(5):
        available = choice(AVAILABILITY)[0]
        data: list = [fake.word(), fake.name(), available]
        if available != "free":
            if available == "reading":
                date: str = f'2023-{str(randint(1,6)).zfill(2)}-{str(randint(1,30)).zfill(2)}'
            else:
                date: str = f'2023-{str(randint(7,12)).zfill(2)}-{str(randint(1,30)).zfill(2)}'
            data.append(date)
        fake_data.append(data)
    return fake_data


async def write_data_to_csv(data: list, mode: Any, name_file: str) -> None:
    async with aiofiles.open(name_file, mode=mode, encoding="utf-8", newline="") as afp:
        writer = AsyncWriter(afp, dialect='unix')
        await writer.writerows(data)


async def main():
    await write_data_to_csv(create_fake_readers(), "w", "readers.csv")
    await write_data_to_csv(create_fake_books(), "w", "books.csv")
    for _ in range(1):
        await write_data_to_csv(create_fake_readers(), "a", "readers.csv")
        await write_data_to_csv(create_fake_books(), "a", "books.csv")


asyncio.run(main())

