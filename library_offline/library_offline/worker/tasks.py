import asyncio
from datetime import datetime, timedelta, date

from celery import shared_task
import aiofiles
from aiocsv import AsyncReader

from django.core.mail import send_mass_mail

from library.models import Books, Readers


async def reading_csv(file_name) -> list:
    async with aiofiles.open(f"library/upload/{file_name}", mode="r", encoding="utf-8", newline="") as afp:
        data: list = [row async for row in AsyncReader(afp)]
    return data


def run_reading_csv(file_name):
    return(asyncio.run(reading_csv(file_name)))

@shared_task
def import_csv():
    books = run_reading_csv("books.csv")
    temp = []
    for book in books:
        try:
            date = book[3]
            date_receipt = datetime.strptime(date, '%Y-%m-%d')
            date_return = date_receipt + timedelta(days=14)
            temp.append(Books(title=book[0], author=book[1], availability=book[2],
                              date_of_receipt=date_receipt, planned_return_date=date_return))
        except IndexError:
            temp.append(Books(title=book[0], author=book[1], availability=book[2]))
    Books.objects.bulk_create(temp)

@shared_task
def import_csv_readers():
    readers = run_reading_csv("readers.csv")
    temp = []
    for reader in readers:
        temp.append(Readers(readers_name=reader[0], address=reader[1], mail=reader[2]))
    Readers.objects.bulk_create(temp)


@shared_task
def send_mail_to_debtors():
    date_today = date.today()
    delta_date = date_today - timedelta(days=14)
    get_debtors = Readers.objects.filter(books__availability="reading",
                                               books__date_of_receipt__lte=delta_date).values("mail","readers_name")
    subject = "you have books"
    messages = ([[subject, f'Уважаемый(я)  { debtor.get("readers_name")}. У вас находится книга более 14 дней', debtor.get("mail"), [debtor.get("mail")]] for debtor in get_debtors])
    send_mass_mail(messages, fail_silently=False)


