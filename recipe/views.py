from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

import recipe
from .models import *
from .serializers import *
from rest_framework import status
import random



class GetAllCategories(APIView):
    
    def get(self, request):
        cat = Category.objects.all()
        cat = CategorySerializer(cat, many=True)
        return Response({
            "status":status.HTTP_200_OK,
            "data":cat.data
        }, status.HTTP_200_OK)

class GetCategoryRecipes(APIView):
    

    def get(self,request, id):
        cat = Category.objects.get(id=id)
        recipes = list(reversed(cat.recipes.all()))
        data = RecipeSerializer(recipes, many=True)
        return Response({
            "status":status.HTTP_200_OK,
            "data":data.data
        }, status=status.HTTP_200_OK)

class GetAllRecipes(APIView):
    def get(self, request):
        recipes = Recipe.objects.all()

        recipes = RecipeSerializer(recipes, many=True)

        return Response({
            "status":status.HTTP_200_OK,
            "data":recipes.data
        }, status=status.HTTP_200_OK)

class GetRecipeDetail(APIView):

    def get(self, request, id):
        recipe = Recipe.objects.get(id=id)
        recipe = RecipeSerializer(recipe)

        return Response({
            "status":status.HTTP_200_OK,
            "data":recipe.data
        })

class SaveRecipe(APIView):
    
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
    

    def get(self, request, email):
        user = User.objects.get(email=email)
        sr = SavedRecipe.objects.filter(user=user)

        data = SavedRecipeSerializer(sr, many=True)
        
        return Response({
            "status":status.HTTP_200_OK,
            "data":data.data
        })


class RemoveSavedRecipe(APIView):
    

    def post(self, request, id):
        sr = SavedRecipe.objects.get(id=id)
        sr.delete()

        return Response({
            "status":status.HTTP_200_OK,
            "message":"Recipe has been removed."
        })

class AddReview(APIView):
    def post(self, request):
        data = AddReviewSerializer(request.data).data

        user = User.objects.get(email=data['email'])
        recipe = Recipe.objects.get(id=data['recipe_id'])

        review = Review.objects.create(user=user, text=data['text'])
        review.save()

        recipe.reviews.add(review)
        recipe.save()

        if user in recipe.raters.all():
            rating = recipe.all_ratings.get(user__id=user.id)
            print()
            rating.rate = data['rate']
            rating.save()
        
        else:
            # print(float(data['rate']))
            rating = Rating.objects.create(user=user,rate=float(data['rate'])) 
            rating.save()

            recipe.all_ratings.add(rating)
            recipe.raters.add(user)
            recipe.raters_ids.add(user.id)

            recipe.save()

        return Response({
            "status":status.HTTP_200_OK,
            "message":"Thank you for your feedback"
        })


class RateRecipe(APIView):

    def post(self, request):
        data = request.data

        user = User.objects.get(email=data['email'])
        recipe = Recipe.objects.get(id=data['recipe_id'])

        if user in recipe.raters.all():
            rating = recipe.all_ratings.get(user__id=user.id)
            print()
            rating.rate = data['rate']
            rating.save()

            return Response({
                "status":status.HTTP_200_OK,
                "message":"Thank you for rating this recipe."
            })
        
        
        else:
            # print(float(data['rate']))
            rating = Rating.objects.create(user=user,rate=float(data['rate'])) 
            rating.save()

            recipe.all_ratings.add(rating)
            recipe.raters.add(user)
            recipe.raters_ids.add(user.id)

            recipe.save()
            return Response({
                "status":status.HTTP_200_OK,
                "message":"Thank you for rating this recipe."
            })


class AddChefTips(APIView):
    

    def post(self, request):
        data = AddTipSerializer(request.data).data

        email = data['email']
        user = User.objects.get(email=email)
        recipe = Recipe.objects.get(id=data['recipe_id'])
        text = data['text']

        tip = Tip.objects.create(
            user=user,
            text=text
        )
        tip.save()


        recipe.tips_from_chef.add(tip)
        recipe.save()

        return Response({
            "status":status.HTTP_200_OK,
            "message":"Thank you for the tip."
        })

class GetFeaturedRecipes(APIView):
    def get(self, request):
        recipes = Recipe.objects.filter(featured=True)

        recipes = RecipeSerializer(recipes, many=True)

        return Response({
            "status":status.HTTP_200_OK,
            "data":recipes.data
        }, status=status.HTTP_200_OK)


class GetRecommendedRecipes(APIView):
    def get(self, request, email):
        recipes = Recipe.objects.all()
        random.shuffle(recipes)
        recipes = RecipeSerializer(recipes, many=True)

        return Response({
            "status":status.HTTP_200_OK,
            "data":recipes.data
        }, status=status.HTTP_200_OK)


class GetscheduledRecipes(APIView):
    def get(self, request, email):
        try:
            user = User.objects.get(email=email)
            recipes = ScheduledRecipe.objects.filter(user=user)
            recipes = ListSchedRecipesSerializer(recipes, many=True)

            return Response({
                "status":status.HTTP_200_OK,
                "data":recipes.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status":status.HTTP_400_BAD_REQUEST,
                "message":"Sorry, something went wrong"
            }, status=status.HTTP_400_BAD_REQUEST)

class CreateScheduledRecipe(APIView):
    def post(self, request):
        
        try:
            data = ScheduleRecipeSerializer(data=request.data)
            data.is_valid(raise_exception=True)

            data = data.data

            user = User.objects.get(email=data['user_email'])
            recipe = Recipe.objects.get(id=data['recipe_id'])
            date = data['date']

            obj = ScheduledRecipe.objects.create(
                user=user,
                recipe=recipe,
                date_to_order=date
            )
            obj.save()
            return Response(
                {
                    "status":status.HTTP_200_OK,
                    "message":"Successful"
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            print(e)
            return Response(
                {
                    "status":status.HTTP_400_BAD_REQUEST,
                    "message":"Unsuccessful"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

class ListAllEvent(APIView):
    
    def get(self, request):
        events = Event.objects.all()

        events = ListEventSerializer(events, many=True)

        return Response(
            {
                "status":status.HTTP_200_OK,
                "data":events.data
            },
            status=status.HTTP_200_OK
        )

class EventRecipesView(APIView):

    def get(self, request, id):
        try:
            event = Event.objects.get(id=id)
            event = ListEventSerializer(event)
            return Response(
                {
                    "status":status.HTTP_200_OK,
                    "data":event.data
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

