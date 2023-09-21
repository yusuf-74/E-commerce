# TOKEN IMPORTS
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
# OAUTH2 IMPORTS
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from decouple import config
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
# LOCAL IMPORTS
from .serializers import UserSerializer, OneTimePassCodeSerializer
from .models import User,OneTimePassCode
from.tasks import send_verification_email
from .models import AuthProvider
from .utils.user_data_generator import create_user_name

import random
import requests 


class SignUpView(APIView):
    def post(self, request):
        # get the data from the request and validate it then save it
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            # create otp for the user and associate it with the user
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
    authentication_classes = []
    permission_classes = []
    def post(self, request,*args, **kwargs):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            # if the user is not verified then return not verified error
            if user.is_verified:
                refresh = RefreshToken.for_user(user)
                user_data = UserSerializer(user).data
                refresh_token = str(refresh)
                access_token = str(refresh.access_token)
                
                response_data = {
                    'refresh_token': refresh_token,
                    'access_token': access_token,
                }
                response_data.update(user_data)
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Account is not verified'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request,*args, **kwargs):
        
        otp = request.GET.get('otp')
        user_id = request.GET.get('user_id')
        try :
            # if the otp is valid then verify the user
            # and mark the otp as used
            otp = OneTimePassCode.objects.get(user_id=user_id , otp=otp , is_used=False)
            user = User.objects.get(pk=user_id)
            
            user.is_verified = True
            user.save()
            otp.is_used = True
            otp.save()
            return Response({'message': 'Account verified successfully'}, status=status.HTTP_200_OK)
            
        except User.DoesNotExist or OneTimePassCode.DoesNotExist:
            return Response({'error': 'Invalid URL'}, status=status.HTTP_400_BAD_REQUEST)

class LoginWithGoogleView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request,*args, **kwargs):
        token = request.data["credential"]
        try: 
            idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), config('GOOGLE_CLIENT_ID'))
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        
        email = idinfo['email']
        first_name = idinfo['given_name']
        last_name = idinfo['family_name']
        
        user = User.objects.filter(email=email).first()
        # if the user exists then login the user and mark the user as verified
        if user:
            user.is_verified = True
            user.save()
            token = RefreshToken.for_user(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            user_data = UserSerializer(user).data
            response_data = {
                "user": user_data,
                "refresh_token": refresh_token,
                "access_token": access_token,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            user = User.objects.create(username = create_user_name(first_name=first_name , last_name=last_name),email=email,first_name=first_name,last_name=last_name , password=random.randint(1,99999999), is_verified=True)
            
            token = RefreshToken.for_user(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            
            user_data = UserSerializer(user).data
            
            response_data = {
                "user": user_data,
                "refresh_token": refresh_token,
                "access_token": access_token,
            }
            return Response(response_data, status=status.HTTP_200_OK)


class GoogleExchangeCodeForTokenView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request,*args, **kwargs):
        # scopes is a list of permissions that the user granted access to
        scopes = request.data.get('scopes')
        
        try:
            # get the access token and refresh token from the code
            flow = Flow.from_client_secrets_file(
                'client_secrets.json',
                scopes=scopes,
            )
            flow.redirect_uri = 'http://localhost'
            creds = flow.fetch_token(code=request.data.get('code'))


            access_token = creds.get('access_token')
            refresh_token = creds.get('refresh_token')
            
            user = request.user
            
            if not user.auth_providers.filter(provider='google').exists():
                AuthProvider.objects.create(
                    provider='google',
                    user=user,
                    access_token=access_token,
                    refresh_token=refresh_token
                )
            else :
                auth_provider = AuthProvider.objects.filter(user=user).first()
                auth_provider.access_token = access_token
                auth_provider.refresh_token = refresh_token
                auth_provider.save()
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(user.json(), status=status.HTTP_200_OK)

# JUST FOR TESTING
class IsAuthenticatedView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request,*args, **kwargs):
        return Response({'message': 'Authenticated'}, status=status.HTTP_200_OK)



@api_view(['GET'])
def get_calender_events(request):
    auth_provider = AuthProvider.objects.filter(user=request.user).first()
    if auth_provider:
        access_token = auth_provider.access_token
        refresh_token = auth_provider.refresh_token
        
        creds = Credentials(token = access_token, refresh_token=refresh_token,token_uri=config('GOOGLE_TOKEN_URI') ,client_id=config('GOOGLE_CLIENT_ID'),client_secret=config('GOOGLE_CLIENT_SECRET'), scopes=['https://www.googleapis.com/auth/calendar'])
        
        service = build('calendar', 'v3', credentials=creds)
        
        events = service.events().list(  calendarId='primary', 
                                maxResults=10, 
                                singleEvents=True,
                                orderBy='startTime').execute()

        if events:
            return Response(events, status=status.HTTP_200_OK)
        else:
            return Response(events, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'No auth provider found'}, status=status.HTTP_400_BAD_REQUEST)