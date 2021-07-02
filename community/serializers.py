from rest_framework import serializers
from .models import *



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields="__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields="__all__"

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(read_only=True, many=True)
    class Meta:
        model=Post
        fields = "__all__"


class CommentSerializer(serializers.Serializer):
    post_id = serializers.IntegerField()
    email = serializers.EmailField()
    comment = serializers.CharField()