from rest_framework import serializers
from .models import *

class CommentSerializer(serializers.ModelSerializer):
    writer = serializers.CharField(source='writer.username', read_only=True)

    class Meta:
        model = Comment
        fields= '__all__'
        read_only_fields = ['post','writer']

class PostSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only = True)
    created_at = serializers.CharField(read_only=True)
    updated_at = serializers.CharField(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)
    writer = serializers.CharField(source='writer.username', read_only=True)

    def get_comments(self, instance):
        serializer = CommentSerializer(instance.comments, many=True)
        return serializer.data
    
    class Meta:
        model = Post
        fields='__all__'
        read_only_fields=[
            'id',
            'created_at',
            'updated-at',
            'comments',
            'writer',
            'like_num'
        ]


class PostListSerializer(serializers.ModelSerializer):
    comments_cnt = serializers.SerializerMethodField()
    
    def get_comments_cnt(self, instance):
        return instance.comments.count()
    
    class Meta:
        model = Post
        fields = [
            "id",
            "writer",
            "created_at",
            "updated_at",
            "comments_cnt",
            "like_num"
        ]
        read_only_fields = ["id", "created_at", "updated_at", "comments_cnt","like_num"]