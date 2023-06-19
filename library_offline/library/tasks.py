from datetime import datetime, timedelta

from celery import shared_task

from library.models import Books, Readers
from library.utils.import_from_csv import run_reading_csv


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
