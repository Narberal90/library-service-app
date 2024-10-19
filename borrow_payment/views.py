import stripe
from django.http import JsonResponse, HttpRequest
from flask import redirect
from rest_framework import views
from django.conf import settings


stripe.api_key = settings.STRIPE_SECRET_KEY
DOMAIN = "http://localhost:8000"


def create_checkout_session(request: HttpRequest, borrowing_id: int):
    checkout_session = stripe.checkout.Session.create(
        line_items=[
            {
                # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                'price': 'price_1QBZQUJwyg37szRjxxuZZtwU',
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url=DOMAIN + '/success',
        cancel_url=DOMAIN + '/cancel',
    )
    breakpoint()
    return redirect(checkout_session.url)


class CreateCheckoutSessionView(views.APIView):

    def post(self, request):
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    "price": "{{PRICE_ID}}",
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url=self.DOMAIN + "/success.html",
            cancel_url=self.DOMAIN  + "/cancel.html",
        )
        return JsonResponse({
            "id": checkout_session.id
        })
