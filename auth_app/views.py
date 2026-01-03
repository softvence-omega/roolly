from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, LoginSerializer, SendOTPSerializer, VerifyOTPSerializer, UpdateUserSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .models import OTP, Profile
from django.core.mail import send_mail
from random import randint
from django.utils import timezone
from datetime import timedelta


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(username=serializer.data['username'], password=serializer.data['password'])
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SendOTPView(APIView):
    serializer_class = SendOTPSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data.get('email')
        phone = serializer.validated_data.get('phone')
        user = None
        
        if email:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        elif phone:
            try:
                profile = Profile.objects.get(phone=phone)
                user = profile.user
            except Profile.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        otp_code = randint(100000, 999999)
        OTP.objects.create(user=user, otp=str(otp_code))

        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp_code}',
            'from@example.com',
            [user.email],
            fail_silently=False,
        )

        return Response({'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)


class VerifyOTPView(APIView):
    serializer_class = VerifyOTPSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data.get('email')
        phone = serializer.validated_data.get('phone')
        otp_code = serializer.validated_data['otp']
        user = None

        if email:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        elif phone:
            try:
                profile = Profile.objects.get(phone=phone)
                user = profile.user
            except Profile.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        five_minutes_ago = timezone.now() - timedelta(minutes=5)
        otp = OTP.objects.filter(user=user, otp=otp_code, created_at__gte=five_minutes_ago).first()

        if otp:
            token, created = Token.objects.get_or_create(user=user)
            otp.delete()
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid or expired OTP'}, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserAPIView(generics.UpdateAPIView):
    serializer_class = UpdateUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user