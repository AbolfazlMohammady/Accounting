from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser , FormParser

from .models import Post, Comment
from .permission import IsOwnerOrReadOnly
from .serializer import CommentSerializer, PostSerializer, CustomPostSerializer, CreatePostSerializer, UpdatePostSerializer

class PostViewSet(ModelViewSet):
    # parser_classes = [MultiPartParser, FormParser]
    permission_classes= [IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            if self.request.user.is_staff:
                return CustomPostSerializer
        if self.action == 'create':
            return CreatePostSerializer
        if self.action == 'update' and self.request.user.is_staff:
            return UpdatePostSerializer
        return PostSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Post.objects.select_related('author').all().order_by('-update_at')
        return Post.objects.select_related('author').filter(status='P').order_by('-update_at')
    
    def update(self, request, *args, **kwargs):
        partial = True
        return super().update(request, partial=partial, *args, **kwargs)
    

# class CommentViewSet(ModelViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer