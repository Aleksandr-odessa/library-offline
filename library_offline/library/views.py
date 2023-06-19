from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from library.models import Books, Readers
from library.serializers import (BooksSerializer, ReadersSerializer,
                                 UploadSerializer)
from library.tasks import import_csv, import_csv_readers
from library.utils.utils import create_dict_for_output, serach_nearest_book


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
        books_reserved_temp = Books.objects.filter(availability="reserved").values()
        books_reading_temp = Books.objects.filter(availability="reading").values()
        books_reserved = create_dict_for_output(books_reserved_temp)
        books_reading = create_dict_for_output(books_reading_temp)
        return Response({"reserved": books_reserved, "reading": books_reading})


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
        return Response("success")

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
        return Response("success")