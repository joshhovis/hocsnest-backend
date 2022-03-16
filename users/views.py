import imp
from urllib import request
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from .models import NewUser
from .serializers import MyTokenObtainPairSerializer
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async

class ObtainTokenPairWithColorView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class CustomUserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAndBlacklistRefreshTokenForUserView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ObtainNewUserToken(APIView):
    create_user_token = {}

    @database_sync_to_async
    def get_tokens_for_user(self, user_id):
        user_id = 1
        try:
            refresh = RefreshToken.for_user(get_user_model().objects.get(id=user_id))
            return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        except get_user_model().DoesNotExist:
            print('error')




