from django.db.models import F
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, permissions
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser , FormParser
from rest_framework.viewsets import ModelViewSet, GenericViewSet, mixins
from django_filters.rest_framework import DjangoFilterBackend

from .models import Post, Comment
from .permission import IsOwnerOrReadOnly
from .serializer import( 
                        PostSerializer, 
                        CommentSerializer, 
                        CustomPostSerializer, 
                        CreatePostSerializer, 
                        UpdatePostSerializer,
                        RetrievePostSerializer
                        )

class PostPagination(PageNumberPagination):
    page_size = 7
    page_size_query_param = 'page_size'
    max_page_size = 100


class PostViewSet(ModelViewSet):
    # parser_classes = [MultiPartParser, FormParser]
    # permission_classes= [IsOwnerOrReadOnly]
    pagination_class = PostPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category', 'title']
    search_fields = ['title', 'category']

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
    
    
    def retrieve(self, request, *args, **kwargs):
        post = self.get_object()
        Post.objects.filter(id=post.id).update(views=F('views') + 1)
        post.refresh_from_db()

        serializer = self.get_serializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user

        # چک کردن اینکه کاربر قبلاً لایک کرده یا نه
        if user in post.liked_users.all():
            return Response({"detail": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        # اضافه کردن کاربر به لیست لایک‌ها
        post.liked_users.add(user)
        post.like_count += 1 
        post.save()

        return Response({"detail": "Post liked successfully."}, status=status.HTTP_200_OK)
    


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
    
