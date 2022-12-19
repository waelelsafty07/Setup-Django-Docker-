from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import Users
from .serializers import LoginSerializer, RegisterSerializer, UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from knox.auth import AuthToken
from django.contrib.auth import login
from Utils.RespnseMessage import RespnseMessage


class overserialzer(AuthTokenSerializer):
    def validated_data(self, user):
        print(user)


class RegisterView(APIView, RespnseMessage):
    permission_classes = [AllowAny]

    def SendResposne(self, user, status):
        message = user
        return Response(message, status=status)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return self.SendResposne(serializer.data, 201)


class LoginView(KnoxLoginView, RespnseMessage):
    permission_classes = [AllowAny]

    def SendResposne(self, message, status):
        return Response(message, status)

    def post(self, request):

        serializer = LoginSerializer(
            data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer = serializer.validated_data
        user, message = serializer
        _, token = AuthToken.objects.create(user)

        login(request, user)
        if message:
            message = {"message": message}
            return self.SendResposne(message, 200)
        user = UserSerializer(user)
        message = {"token": token, "user": user.data}
        return self.SendResposne(message, 200)
