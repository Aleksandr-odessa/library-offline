from django.db import models

from library.utils.data import AVAILABILITY


class Readers(models.Model):
    readers_name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=50)
    mail = models.EmailField(unique=True)

    def __str__(self):
        return self.readers_name


class Books(models.Model):
    title = models.CharField("Название книги", max_length=25)
    author = models.CharField("Автор", max_length=50)
    availability = models.CharField("Наличие книги", choices=AVAILABILITY, default='free',max_length=15)
    date_of_receipt = models.DateField("Дата выдачи читателю", null=True)
    planned_return_date = models.DateField("Планируемая дата возврата", null=True)
    readers = models.ForeignKey(Readers,verbose_name="reader", to_field="readers_name", on_delete=models.CASCADE, null=True)


