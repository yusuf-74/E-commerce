from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignUpSerializer, OneTimePassCodeSerializer
from .models import User,OneTimePassCode
from.tasks import send_verification_email
import random

class SignUpView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            random_otp = random.randint(100000,999999)
            otp_serializer = OneTimePassCodeSerializer(data={"user":serializer.instance.pk , "otp":random_otp})
            
            if otp_serializer.is_valid():
                otp_serializer.save()

            
            # send otp to user
            send_verification_email.delay(serializer.instance.email , serializer.instance.pk, random_otp)
            
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request,*args, **kwargs):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        
        user = authenticate(username=username, password=password)
        if user:
            
            if user.is_verified:
                refresh = RefreshToken.for_user(user)
                
                refresh_token = str(refresh)
                access_token = str(refresh.access_token)
                response_data = {
                    'refresh_token': refresh_token,
                    'access_token': access_token,
                }
                
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Account is not verified'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(APIView):
    def get(self, request,*args, **kwargs):
        otp = request.GET.get('otp')
        user_id = request.GET.get('user_id')
        try :
            # otp = OneTimePassCode.objects.get(user_id=user_id , otp=otp , is_used=False)
            # user = User.objects.get(pk=user_id)
            
            # user.is_verified = True
            # user.save()
            # otp.is_used = True
            # otp.save()
            return Response({'message': 'Account verified successfully'}, status=status.HTTP_200_OK)
            
        except User.DoesNotExist or OneTimePassCode.DoesNotExist:
            return Response({'error': 'Invalid URL'}, status=status.HTTP_400_BAD_REQUEST)
        