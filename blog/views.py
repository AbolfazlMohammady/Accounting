from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.viewsets import ModelViewSet, GenericViewSet, mixins
from rest_framework.parsers import MultiPartParser , FormParser

from .models import Post, Comment
from .permission import IsOwnerOrReadOnly, IsOwnerOrReadOnlyComment
from .serializer import( 
                        PostSerializer, 
                        CommentSerializer, 
                        CustomPostSerializer, 
                        CreatePostSerializer, 
                        UpdatePostSerializer,
                        RetrievePostSerializer
                        )


class PostViewSet(ModelViewSet):
    # parser_classes = [MultiPartParser, FormParser]
    # permission_classes= [IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            if self.request.user.is_staff:
                return CustomPostSerializer
        if self.action == 'create':
            return CreatePostSerializer
        if self.action == 'update' and self.request.user.is_staff:
            return UpdatePostSerializer
        if self.action == 'retrieve':
            return RetrievePostSerializer
        return PostSerializer


    def get_permissions(self):
        if self.action == 'create' or self.action== 'update' or self.action == 'delete':
            return  [permissions.IsAuthenticated(),IsOwnerOrReadOnly()]
        return [IsOwnerOrReadOnly()]



    def get_queryset(self):
        if self.request.user.is_staff:
            return Post.objects.select_related('author').prefetch_related('comments').all().order_by('-update_at')
        return Post.objects.select_related('author').prefetch_related('comments').filter(status='P').order_by('-update_at')
    
    def update(self, request, *args, **kwargs):
        partial = True
        return super().update(request, partial=partial, *args, **kwargs)
    

class CommentViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = Comment.objects.select_related('user','post').all()
    serializer_class = CommentSerializer

    
    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.IsAuthenticated()]
        if self.request.method in ['DELETE', 'PUT', 'PATCH']:
            return [permissions.IsAdminUser()]
        return super().get_permissions()