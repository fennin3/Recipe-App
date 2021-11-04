from django.shortcuts import render
from .serializers import AddressSerializer, CreateUserSerializer, LanguageSerializer, PaymentSerializer, UserLoginSerializer, UserSerializer
from rest_framework.views import APIView
from django.contrib.auth import authenticate, get_user_model
from rest_framework.response import Response
from rest_framework import status
from .utils import sending_mail, generate_OTP
from .models import Address, OTPCode, Language, PaymentMethods

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
            try:
                code = generate_OTP()
                sending_mail(f"Your email verification code is {code}", "Email Verification", email)
                otp = OTPCode.objects.create(code=code, email=email)
                otp.save()

                return Response(
                    {
                        "status":status.HTTP_400_BAD_REQUEST,
                        "message":"You have to verify your account.",
                        "email_verified":True
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            except Exception as e:
                return Response(
                    {
                        "status":status.HTTP_400_BAD_REQUEST,
                        "message":"Sorry, something went wrong try again.",
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
        if code == '12345' and email=="esswordorg@gmail.com":
            print("wan pen")
        else:
            print("not wan pen")
        try:
            code = OTPCode.objects.get(code=str(code).strip(), email=str(email).strip())
            code.delete()
            user = User.objects.get(email=str(email).strip())

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

class UserDetailView(APIView):


    def get(self, request, email):
        try:
            user = User.objects.get(email=email)
            data = UserSerializer(user)
    

            return Response({
                "status":status.HTTP_200_OK,
                "data":data.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({
                "status":status.HTTP_400_BAD_REQUEST,
                "message":"Sorry, an error occured"
            }, status=status.HTTP_400_BAD_REQUEST)

class RequestPasswordResetCode(APIView):
    permission_classes=()
    def post(self, request):
        try:
            email = request.data['email']

            user = User.objects.filter(email=email)

            if user.count() < 1:
                return Response(
                    {
                        "status":status.HTTP_400_BAD_REQUEST,
                        "message":"Sorry, there is no user with the email provided."

                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                user = user.first()
                code = generate_OTP()
                sending_mail(f"Your password reset code is {code}", "Password Reset", user.email)
                otp = OTPCode.objects.create(code=code, email=user.email)
                otp.save()
                
                return Response(
                    {
                        "status":status.HTTP_200_OK,
                        "message":"We have sent a password reset code to the provided email, please check your mail."
                    },
                    status=status.HTTP_200_OK
                )
        except Exception as e:
            print(e)
            return Response(
                    {
                        "status":status.HTTP_400_BAD_REQUEST,
                        "message":"Please something went wrong, try again later."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

class PasswordReset(APIView):
    permission_classes = ()

    def post(self, request):
        try:
            email = request.data['email']
            code = request.data['code']
            password = request.data['password']

            user = User.objects.filter(email=email)
            try:
                code_otp = OTPCode.objects.get(code=code, email=email)
                code_otp.delete()
            except Exception as e:
                return Response(
                {
                    "status":status.HTTP_400_BAD_REQUEST,
                    "message":"Invalid code"
                },
                status=status.HTTP_400_BAD_REQUEST
                )
            
            user=user.first()
            user.set_password(password)
            user.save()

            return Response(
                    {
                        "status":status.HTTP_200_OK,
                        "message":"Your password has been changed"
                    },
                    status=status.HTTP_200_OK
                )
        except Exception as e:
            print(e)
            return Response(
                    {
                        "status":status.HTTP_400_BAD_REQUEST,
                        "message":"Sorry, something went wrong."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

class RetrievePaymentMethods(APIView):
    def get(self, request, email):
        try:
            user = User.objects.get(email=email)  

            pms = PaymentMethods.objects.filter(user=user)

            pms = PaymentSerializer(pms, many=True)

            return Response(
                {
                    "status":status.HTTP_200_OK,
                    "data":pms.data
                },
                status=status.HTTP_200_OK
            )   
        except Exception as e:
            return Response(
                {
                    "status":status.HTTP_400_BAD_REQUEST,
                    "message":"Sorry, something went wrong"
                },
                status=status.HTTP_400_BAD_REQUEST
            )   
            

class RetrieveAddresses(APIView):
    def get(self, request, email):
        try:
            user = User.objects.get(email=email)  

            adds = Address.objects.filter(user=user)

            adds = AddressSerializer(adds, many=True)

            return Response(
                {
                    "status":status.HTTP_200_OK,
                    "data":adds.data
                },
                status=status.HTTP_200_OK
            )   
        except Exception as e:
            return Response(
                {
                    "status":status.HTTP_400_BAD_REQUEST,
                    "message":"Sorry, something went wrong"
                },
                status=status.HTTP_400_BAD_REQUEST
            )   
            
class AddPaymentMethods(APIView):

    def post(self, request):
        email = request.data.get('email', None)
        type = request.data.get('type', None)
        momo_name = request.data.get('momo_name', None)
        momo_num = request.data.get('momo_num', None)
        holder_name = request.data.get('holder_name', None)
        card_num = request.data.get('card_num', None)
        exp_month = request.data.get('exp_month', None)
        exp_year = request.data.get('exp_year', None)
        print(type)
        if email is None:
            return Response(
                {
                    "status":status.HTTP_400_BAD_REQUEST,
                    "message":"Email is required"
                }, status=status.HTTP_400_BAD_REQUEST
            )

        if type is None:
            return Response(
                {
                    "status":status.HTTP_400_BAD_REQUEST,
                    "message":"Payment type is required"
                }, status=status.HTTP_400_BAD_REQUEST
            )
    
        elif str(type).lower() == 'card' and ((holder_name is None or holder_name == "") or (card_num is None or card_num == "")):
            return Response(
                {
                    "status":status.HTTP_400_BAD_REQUEST,
                    "message":"Card holder name and card number can not be empty"
                }, status=status.HTTP_400_BAD_REQUEST
            )
        elif str(type).lower() == 'momo' and ((momo_name is None or momo_name == "") or (momo_num is None or momo_num == "")):
            return Response(
                {
                    "status":status.HTTP_400_BAD_REQUEST,
                    "message":"momo name and momo number can not be empty"
                }, status=status.HTTP_400_BAD_REQUEST
            )
        
        user = User.objects.get(email=email)
        pms = PaymentMethods.objects.create(
            user=user,
            type=type,
            momo_number=momo_num,
            momo_name=momo_name,
            holder_name=holder_name,
            card_number=card_num,
            exp_month=exp_month,
            exp_year=exp_year
        )

        pms.save()

        return Response(
                {
                    "status":status.HTTP_200_OK,
                    "message":"Payment method has been saved"
                }, status=status.HTTP_200_OK
            )
        
class AddAddress(APIView):
    def post(self, request):
        email = request.data.get('email', None)
        name = request.data.get('name', None)
        reci_name = request.data.get('recipient_name', None)
        reci_num = request.data.get('recipient_phone', None)
        address = request.data.get('address', None)
        area = request.data.get('area', None)
        city = request.data.get('city', None)
        defaul = request.data.get('default', None)
        # instruction = request.data.get('instruction', None)

        if email is None:
            return Response(
                {
                    "status":status.HTTP_400_BAD_REQUEST,
                    "message":"Email is required"
                }, status=status.HTTP_400_BAD_REQUEST
            )

        if reci_num is None or reci_num=="":
            return Response(
                {
                    "status":status.HTTP_400_BAD_REQUEST,
                    "message":"Recipient number can not be empty"
                }, status=status.HTTP_400_BAD_REQUEST
            )
        
        if reci_name is None or reci_name=="":
            return Response(
                {
                    "status":status.HTTP_400_BAD_REQUEST,
                    "message":"Recipient name can not be empty"
                }, status=status.HTTP_400_BAD_REQUEST
            )
        if address is None or "":
            return Response(
                {
                    "status":status.HTTP_400_BAD_REQUEST,
                    "message":"Address can not be empty"
                }, status=status.HTTP_400_BAD_REQUEST
            )    
        
        user = User.objects.get(email=email)
        if defaul:
            for add in user.addresses.all():
                add.default =False
                add.save()

        adds = Address.objects.create(
            user=user,
            name=name,
            recipient_name=reci_name,
            recipient_phone=reci_num,
            address=address,
            area=area,
            city=city,
            # instruction=instruction,
            default=defaul
        )

        adds.save()

        return Response(
                {
                    "status":status.HTTP_200_OK,
                    "message":"Address has been saved"
                }, status=status.HTTP_200_OK
            )


