from rest_framework.fields import FileField
from rest_framework.serializers import ModelSerializer, Serializer

from library.models import Books, Readers


class BooksSerializer(ModelSerializer):
    class Meta:
        model = Books
        fields = "__all__"


class ReadersSerializer(ModelSerializer):
    class Meta:
        model = Readers
        fields = "__all__"

class UploadSerializer(Serializer):
    file_uploaded = FileField()
    class Meta:
        fields = ['file_uploaded']