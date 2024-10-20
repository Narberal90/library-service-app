from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from users.serializers import UserSerializer, AuthTokenSerializer
from .models import User


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = []


class LoginUserView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = AuthTokenSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UpdateTelegramIDView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        telegram_id = request.data.get("telegram_id")

        try:
            user = User.objects.get(email=email)
            user.telegram_id = telegram_id
            user.save()
            return Response(
                {"message": "Telegram ID updated!"},
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                {"error": "No user with this email address was found."},
                status=status.HTTP_404_NOT_FOUND
            )
