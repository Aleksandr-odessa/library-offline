from django.urls import include, path
from rest_framework import routers

from library import views

router = routers.DefaultRouter()
router.register(r'books', views.BooksViewSet)
router.register(r'readers', views.ReadersViewSet)
router.register(r'upload_books', views.UploadBooks, basename="upload_books")
router.register(r'upload_readers', views.UploadReaders, basename="upload_readers")

urlpatterns = [
    path('', include(router.urls)),

]

urlpatterns += router.urls