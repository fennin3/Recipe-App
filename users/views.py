from django.shortcuts import render
from .serializers import CreateUserSerializer, LanguageSerializer, UserLoginSerializer
from rest_framework.views import APIView
from django.contrib.auth import authenticate, get_user_model
from rest_framework.response import Response
from rest_framework import status
from .utils import sending_mail, generate_OTP
from .models import OTPCode, Language

from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import update_last_login


User = get_user_model()
JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class CreateUserView(APIView):
    permission_classes=()
    def post(self, request):
        print(request.data)
        data = CreateUserSerializer(data=request.data)

        data.is_valid(raise_exception=True)

        email = data.data['email']

        if User.objects.filter(email=email).exists():
            return Response({
                "status":status.HTTP_400_BAD_REQUEST,
                "message":"Sorry, email already exist."
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            pass


        try:
            code = generate_OTP()
            sending_mail(f"Your email verification code is {code}", "Email Verification", email)
            user = User.objects.create(
                email = email,
                full_name=data.data['full_name'],
                profile_pic = data.data['profile_pic'],
                phone = data.data['phone'],                
                is_active=False
            )
            user.set_password(data.data['password'])
            otp = OTPCode.objects.create(code=code, email=email)
            otp.save()
            user.save()

            return Response({
                "status": status.HTTP_200_OK,
                "message":"Account created successfully."
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({

                "status": status.HTTP_400_BAD_REQUEST,
                "message":"Account creation unsuccessful."
            }, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    queryset = User.objects.all()
    permission_classes = ()
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email']
        password = serializer.data['password']
        
        
        user = authenticate(email=email, password=password)
        #     return Response({
        #         "status":status.HTTP_400_BAD_REQUEST,
        #         "message":"A user with this email and password is not found."
        #     }, status=status.HTTP_400_BAD_REQUEST)

        if user is None:
            return Response({
                "status":status.HTTP_400_BAD_REQUEST,
                "message":"A user with this email and password is not found."
            }, status=status.HTTP_400_BAD_REQUEST)


        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            return Response({
                "status":status.HTTP_400_BAD_REQUEST,
                "message":"A user with this email and password is not found."
            }, status=status.HTTP_400_BAD_REQUEST)
        user_ = User.objects.get(email=email)

        response = {
            'success' : 'True',
            'status' : status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            'token' : jwt_token,
            'id':user_.id,
            'email':user_.email,
            # 'username':user_.username,
            'full_name':user_.full_name,
            # 'profile_pic':user_.profile_pic,
            'phone':user_.phone
            }
        status_code = status.HTTP_200_OK
        if user_.email_verified:
            return Response(response, status=status_code)
        else:
            return Response(
                {
                    "status":status.HTTP_400_BAD_REQUEST,
                    "message":"You have to verify your account.",
                    "email_verified":user_.email_verified,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

class VerifyEmailView(APIView):
    permission_classes=()

    def post(self, request):
        code = request.data['code']
        email = request.data['email']
        print(code)
        print(email)
        try:
            code = OTPCode.objects.get(code=str(code).strip(), email=str(email).strip())
            code.delete()
            user = User.objects.get(email=email)

            user.email_verified=True
            user.is_active=True
            user.save()
            return Response({
                "status":status.HTTP_200_OK,
                "message":"Email has been verified."
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({
                "status":status.HTTP_400_BAD_REQUEST,
                "message":"Invalid Code"
            }, status=status.HTTP_400_BAD_REQUEST)

class SetNotitfications(APIView):
    permission_classes=()

    def put(self, request):
        
        email = request.data['email']
        user = User.objects.get(email=email)
        value = request.data['value']
        value_for = request.data['value_for']

        if value_for.lower() == "not":
            user.notifications = value

            user.save()
        elif value_for.lower() == "news":
            user.email_news = value

            user.save()
        else:
            user.special_offers = value
            user.save()
        
        return Response({
            "status":status.HTTP_200_OK,
            "message":"Changes has been made."
        })


class SetLanguage(APIView): 
    permission_classes=()

    def put(self, request):
        email = request.data['email']
        user = User.objects.get(email=email)

        user.language = request.data['language']

        user.save()

        return Response({
            "status":status.HTTP_200_OK,
            "message":"Changes has been made."
        })  

class RetrieveAllLanguages(APIView):
    permission_classes=()

    def get(self, request):
        lang = Language.objects.all()

        langs = LanguageSerializer(lang, many=True)

        return Response({
            "status":status.HTTP_200_OK,
            "data":langs.data
        })
