from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from books.models import Book
from books.serializers import BookSerializer, BookImageSerializer, BookRetrieveSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return BookSerializer
        elif self.action == "retrieve":
            return BookRetrieveSerializer
        elif self.action == "upload_image":
            return BookImageSerializer

        return BookSerializer

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image"
    )
    def upload_image(self, request, pk=None) -> Response:
        book = self.get_object()
        serializer = self.get_serializer(book, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
