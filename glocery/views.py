import glocery
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework import status



class GetAllCategories(APIView):
    permission_classes=()
    def get(self, request):
        cat = GloceryCategory.objects.all()
        print(cat)
        cate = CategorySerializer(cat, many=True)
        print(cate.data)
        return Response({
            "status":status.HTTP_200_OK,
            "data":cate.data
        }, status.HTTP_200_OK)

class GetCategoryGloceries(APIView):
    permission_classes=()

    def get(self,request, id):
        cat = GloceryCategory.objects.get(id=id)
        gloceries = list(reversed(cat.gloceries.all()))
        data = GlocerySerializer(gloceries, many=True)
        return Response({
            "status":status.HTTP_200_OK,
            "data":data.data
        }, status=status.HTTP_200_OK)

class GetAllGloceries(APIView):
    permission_classes=()
    def get(self, request):
        recipes = Glocery.objects.all()

        recipes = GlocerySerializer(recipes, many=True)

        return Response({
            "status":status.HTTP_200_OK,
            "data":recipes.data
        }, status=status.HTTP_200_OK)

class GetGloceryDetail(APIView):
    permission_classes=()

    def get(self, request, id):
        glo = Glocery.objects.get(id=id)
        glo = GlocerySerializer(glo)

        return Response({
            "status":status.HTTP_200_OK,
            "data":glo.data
        })

class SaveGlocery(APIView):
    permission_classes=()
    def post(self, request):
        data = SaveGlocerySerializer(data=request.data)
        data.is_valid(raise_exception=True)

        email = data.data['email']
        id = data.data['id']

        user = User.objects.get(email=email)
        glocery = Glocery.objects.get(id=id)

        try:
            a = SavedGlocery.objects.filter(glocery=glocery)
            return Response({
                "status":status.HTTP_400_BAD_REQUEST,
                "message":"Glocery has been saved already."
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            saved = SavedGlocery.objects.create(user=user,glocery=glocery)

            saved.save()

            return Response({
                "status":status.HTTP_200_OK,
                "message":"Glocery has been saved."
            })

class GetSavedGlocery(APIView):
    permission_classes=()

    def get(self, request, email):
        user = User.objects.get(email=email)
        sr = SavedGlocery.objects.filter(user=user)

        data = SavedGlocerySerializer(sr, many=True)
        
        return Response({
            "status":status.HTTP_200_OK,
            "data":data.data
        })


class RemoveSavedGlocery(APIView):
    permission_classes=()

    def post(self, request, id):
        sr = SavedGlocery.objects.get(id=id)
        sr.delete()

        return Response({
            "status":status.HTTP_200_OK,
            "message":"Glocery has been removed."
        })