from datetime import date

from library.models import Books


def create_dict_for_output(books_temp: list) -> list:
    books_reading_reserved = []
    for book in books_temp:
        book_read = {'id': book['id'], 'title': book['title'], 'author': book['author'], 'date': book['date_of_receipt']}
        books_reading_reserved.append(book_read)
    return books_reading_reserved

def serach_nearest_book() -> dict| str:
    dict_delta = {}
    date_today = date.today()
    day_today = date_today.day
    month_today = date_today.month
    year_today = date_today.year
    books_three_month = ((Books.objects.filter(availability="reading", planned_return_date__year=year_today)) &
                         ((Books.objects.filter(planned_return_date__month=month_today - 1)) |
                          (Books.objects.filter(planned_return_date__month=month_today)) |
                          (Books.objects.filter(planned_return_date__month=month_today + 1)))). \
        values("id", "planned_return_date")
    if len(books_three_month) == 0:
        return "DB is empty"
    for date_ in books_three_month:
        delta = date_today - date_["planned_return_date"]
        dict_delta[date_["id"]] = int(str(abs(delta))[:2])
    minimum = min(dict_delta, key=dict_delta.get)
    nearest_book = Books.objects.filter(id=minimum).values("id", "title", "planned_return_date")
    return nearest_book