from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .permissions import IsOwnerOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action


from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer,PostListSerializer

# Create your views here.
class TpoLikedPostViewSet(viewsets.ViewSet):
    def list(self, request):
        top_posts = Post.objects.order_by('-like_num')[:3]
        serializer = PostSerializer(top_posts,many=True)
        return Response(serializer.data)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.action =='list':
            return PostListSerializer
        return PostSerializer
    
    def get_permissions(self):
        if self.action in ['update','destroy','partial_update']:
            return [IsAdminUser()]
        return []
    
    def perform_create(self, serializer):
        serializer.save(writer=self.request.user)

    @action(methods=['GET'],detail = False)
    def recommend(self, request):
        ran_post =self.get_queryset().order_by("?").first()
        ran_post_serializer = PostListSerializer(ran_post)
        return Response(ran_post_serializer.data)
    
    @action(methods=['GET'],detail = True)
    def like(self,request, pk=None):
        like_post = self.get_object()
        like_post.like_num +=1
        like_post.save(update_fields = ['like_num'])
        return Response()
    
    
        

class CommentViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ['update','destroy','partial_update']:
            return [IsOwnerOrReadOnly()] #해당 댓글 작성자만 디테일 수정가능 + admin도 가능 
        return []
    
    def perform_create(self, serializer):
        serializer.save(writer=self.request.user)


class PostCommentViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    #queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated] # 로그인한 유저만 댓글 작성가능

    def get_queryset(self):
        post = self.kwargs.get("post_id")
        queryset = Comment.objects.filter(post_id=post)
        return queryset
    
    def create(self, request, post_id=None):
        post = get_object_or_404(Post, id=post_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(writer =request.user ,post=post)
        return Response(serializer.data)
