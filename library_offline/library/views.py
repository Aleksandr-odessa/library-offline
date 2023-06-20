from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet
from datetime import date
from datetime import timedelta
from library.models import Books, Readers
from library.serializers import (BooksSerializer, ReadersSerializer,
                                 UploadSerializer)
from library_offline.worker.tasks import import_csv, import_csv_readers, send_mail_to_debtors

from library.utils.utils import serach_nearest_book


class BooksViewSet(ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer

    @action(detail=False, methods=["get"])
    def count_free_books(self, request):
        count_books = Books.objects.filter(availability="free").count()
        if count_books == 0:
            return Response({"books": serach_nearest_book()})
        return Response({'count_free': count_books})

    @action(detail=False, methods=["get"])
    def book_reserved_reading(self, request):
        books_reserved = Books.objects.filter(availability="reserved").values('id','title','author','date_of_receipt' )
        books_reading = Books.objects.filter(availability="reading").values('id','title','author','date_of_receipt' )
        return Response({"reserved": books_reserved, "reading": books_reading})

    @action(detail=False, methods=["get"])
    def debtors(self, request):
        send_mail_to_debtors.delay()
        return Response("Task accepted. Please wait")


class ReadersViewSet(ModelViewSet):
    queryset = Readers.objects.all()
    serializer_class = ReadersSerializer


class UploadBooks(ViewSet):
    serializer_class = UploadSerializer

    def list(self, request):
        return Response("GET API")

    def create(self, request):
        file_uploaded = request.FILES.get('file_uploaded')
        with open('library/upload/books.csv', 'wb+') as destination:
            for chunk in file_uploaded.chunks():
                destination.write(chunk)
        import_csv.delay()
        return Response("Task accepted. Please wait")

class UploadReaders(ViewSet):
    serializer_class = UploadSerializer

    def list(self, request):
        return Response("GET API")

    def create(self, request):
        file_uploaded = request.FILES.get('file_uploaded')
        with open('library/upload/readers.csv', 'wb+') as destination:
            for chunk in file_uploaded.chunks():
                destination.write(chunk)
        import_csv_readers.delay()
        return Response("Task accepted. Please wait")