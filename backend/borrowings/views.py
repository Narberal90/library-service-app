from django.db import transaction
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema_view
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from books.permissions import IsAdminOrIfAuthenticatedPostAndReadOnly
from borrow_payment.payment_management import manage_checkout_session
from borrowings.models import Borrowing
from borrowings.paginators import BorrowingsPagination
from borrowings.serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingDetailSerializer,
    ReturnBookSerializer,
)


@extend_schema_view(
    list=extend_schema(
        description=(
            "Lists all borrowings. Admins can see all borrowings, while authenticated users can only see "
            "their own. Optionally, borrowings can be filtered by user_id, is_active, or book_title."
        ),
        parameters=[
            OpenApiParameter(
                name="user_id",
                type=OpenApiTypes.INT,
                description="Filter by user ID (admin only)",
            ),
            OpenApiParameter(
                name="is_active",
                type=OpenApiTypes.BOOL,
                description="Filter by active borrowings. Use 'true' for active and 'false' for inactive borrowings, based on actual return date.",
            ),
            OpenApiParameter(
                name="book_title",
                type=OpenApiTypes.STR,
                description="Filter by book title containing the entered text (case-insensitive search)",
            ),
        ],
    ),
    pay_return_borrowing=extend_schema(
        description=(
            "Allows users to mark a borrowing as returned. Optionally, if a 'session_id' matches, it triggers payment for any late returns."
        ),
        parameters=[
            OpenApiParameter(
                name="session_id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Payment session ID",
            ),
        ],
    )
)
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
        return queryset.distinct()

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
