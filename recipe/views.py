import recipe
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework import status



class GetAllCategories(APIView):
    permission_classes=()
    def get(self, request):
        cat = Category.objects.all()
        cat = CategorySerializer(cat, many=True)
        return Response({
            "status":status.HTTP_200_OK,
            "data":cat.data
        }, status.HTTP_200_OK)

class GetCategoryRecipes(APIView):
    permission_classes=()

    def get(self,request, id):
        cat = Category.objects.get(id=id)
        recipes = list(reversed(cat.recipes.all()))
        data = RecipeSerializer(recipes, many=True)
        return Response({
            "status":status.HTTP_200_OK,
            "data":data.data
        }, status=status.HTTP_200_OK)

class GetAllRecipes(APIView):
    permission_classes=()
    def get(self, request):
        recipes = Recipe.objects.all()

        recipes = RecipeSerializer(recipes, many=True)

        return Response({
            "status":status.HTTP_200_OK,
            "data":recipes.data
        }, status=status.HTTP_200_OK)

class GetRecipeDetail(APIView):
    permission_classes=()

    def get(self, request, id):
        recipe = Recipe.objects.get(id=id)
        recipe = RecipeSerializer(recipe)

        return Response({
            "status":status.HTTP_200_OK,
            "data":recipe.data
        })

class SaveRecipe(APIView):
    permission_classes=()
    def post(self, request):
        data = SaveRecipeSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        email = data.data['email']
        id = data.data['id']

        user = User.objects.get(email=email)
        recipe = Recipe.objects.get(id=id)

        saved = SavedRecipe.objects.create(user=user,recipe=recipe)

        saved.save()

        return Response({
            "status":status.HTTP_200_OK,
            "message":"Recipe has been saved."
        })

class GetSavedRecipes(APIView):
    permission_classes=()

    def get(self, request, email):
        user = User.objects.get(email=email)
        sr = SavedRecipe.objects.filter(user=user)

        data = SavedRecipeSerializer(sr, many=True)
        
        return Response({
            "status":status.HTTP_200_OK,
            "data":data.data
        })


class RemoveSavedRecipe(APIView):
    permission_classes=()

    def post(self, request, id):
        sr = SavedRecipe.objects.get(id=id)
        sr.delete()

        return Response({
            "status":status.HTTP_200_OK,
            "message":"Recipe has been removed."
        })