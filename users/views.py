from django.shortcuts import render
from .serializers import CreateUserSerializer, UserLoginSerializer
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from .utils import sending_mail, generate_OTP
from .models import OTPCode

User = get_user_model()

class CreateUserView(APIView):
    permission_classes=()
    def post(self, request):
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

        user = User.objects.create(
            email = email,
            full_name=data.data['full_name'],
            profile_pic = data.data['profile_pic'],
            phone = data.data['phone'],
            notifications = data.data['notifications'],
            email_news = data.data['email_news'],
            special_offers = data.data['special_offers'],
            password = data.data['password'],
            is_active=False
        )

        code = generate_OTP()
        
        try: 
            sending_mail(f"Your email verification code is {code}")
            otp = OTPCode.objects.create(code=code, email=email)
            otp.save()
            user.save()

            return Response({
                "status": status.HTTP_200_OK,
                "message":"Account created successfully."
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message":"Account created successfully."
            }, status=status.HTTP_400_BAD_REQUEST)



class UserLoginView(APIView):
    queryset = User.objects.all()
    permission_classes = ()
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.data)
        email = serializer.data['email']

        user_ = User.objects.get(email=email)

        response = {
            'success' : 'True',
            'status' : status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            'token' : serializer.data['token'],
            'id':user_.id,
            'email':user_.email,
            # 'username':user_.username,
            'full_name':user_.full_name,
            'profile_pic':user_.profile_pic,
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

        try:
            code = OTPCode.objects.get(code=code, email=email)
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
            return Response({
                "status":status.HTTP_400_BAD_REQUEST,
                "message":"Invalid Code"
            }, status=status.HTTP_400_BAD_REQUEST)
