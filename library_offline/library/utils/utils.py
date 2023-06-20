from datetime import date

from library.models import Books


def serach_nearest_book() -> dict| str:
    date_today = date.today()
    nearest_book = Books.objects.filter(availability="reading", planned_return_date__gt=date_today).\
                            order_by("planned_return_date").values("title", "planned_return_date","readers")[:2]
    if nearest_book is None:
        return "DB is empty"
    return nearest_book



