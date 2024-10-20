from django.db import transaction
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from borrowings.paginators import BorrowingsPagination
from books.permissions import IsAdminOrIfAuthenticatedPostAndReadOnly
from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingDetailSerializer,
    ReturnBookSerializer,
)
from borrow_payment.payment_management import manage_checkout_session


class BorrowingViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin
):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = [IsAdminOrIfAuthenticatedPostAndReadOnly]
    pagination_class = BorrowingsPagination

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            borrowing = self.perform_create(serializer)
            manage_checkout_session(borrowing)
            headers = self.get_success_headers(serializer.data)

            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        user = self.request.user
        return serializer.save(user=user)

    def get_queryset(self):
        queryset = super().get_queryset()

        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)

        user_id = self.request.query_params.get("user_id")
        is_active = self.request.query_params.get("is_active")
        book_title = self.request.query_params.get("book_title")

        if self.request.user.is_staff and user_id:
            queryset = queryset.filter(user_id=user_id)

        if is_active:
            if is_active.lower() == "true":
                queryset = queryset.filter(actual_return_date__isnull=True)
            elif is_active.lower() == "false":
                queryset = queryset.filter(actual_return_date__isnull=False)

        if book_title:
            queryset = queryset.filter(book__title__icontains=book_title)
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer
        if self.action == "retrieve":
            return BorrowingDetailSerializer
        if self.action == "pay_return_borrowing":
            return ReturnBookSerializer
        return BorrowingSerializer

    @action(detail=True, methods=["post"], url_path="pay-return")
    def pay_return_borrowing(self, request, pk=None):
        borrowing = self.get_object()
        serializer = self.get_serializer(borrowing, data=request.data)

        serializer.is_valid(raise_exception=True)
        query_session_id = request.query_params.get("session_id")

        if query_session_id == borrowing.payment.session_id:
            borrowing.pay()
        else:
            borrowing.return_book()
            serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
