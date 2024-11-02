from django.urls import path, include
from rest_framework import routers

from borrow_payment.views import PaymentViewSet, success_session

app_name = "borrow_payment"

router = routers.DefaultRouter()
router.register("payment", PaymentViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("success-payment/", success_session, name="success-payment")
]
