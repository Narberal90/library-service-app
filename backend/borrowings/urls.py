from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BorrowingViewSet

router = DefaultRouter()
router.register("borrowings", BorrowingViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
app_name = "borrowing"
