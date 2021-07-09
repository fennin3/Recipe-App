from django.shortcuts import render
from  rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import *
from .models import *



class GetCategories(APIView):
    

    def get(self, request):
        cat = Category.objects.all()

        cat = CategorySerializer(cat, many=True)

        return Response({
            "status":status.HTTP_200_OK,
            "data":cat.data
        })


class GetPostsOfACategory(APIView):
    

    def get(self, request, id):
        cat = Category.objects.get(id=id)
        posts = cat.posts.all()

        posts = PostSerializer(posts, many=True)

        return Response({
            "status":status.HTTP_200_OK,
            "data":posts.data
        })

class GetAllPosts(APIView):
    

    def get(self, request):
        posts = Post.objects.all()

        posts = PostSerializer(posts, many=True)

        return Response({
            "status":status.HTTP_200_OK,
            "data":posts.data
        })


class GetPostDetail(APIView):
    

    def get(self, request, id):
        post = Post.objects.get(id=id)

        post = PostSerializer(post)

        return Response({
            "status":status.HTTP_200_OK,
            "data":post.data
        })


class CommentOnPost(APIView):
    

    def post(self, request):
        data = CommentSerializer(request.data).data

        id = data['post_id']
        email = data['email']
        comment = data['comment']

        post = Post.objects.get(id=id)
        user = User.objects.get(email=email)

        comment = Comment.objects.create(
            user = user,
            text=comment
        )
        comment.save()

        post.comments.add(comment)

        post.save()

        return Response({
            "status":status.HTTP_200_OK,
            "message":"Comment was successful"
        })

