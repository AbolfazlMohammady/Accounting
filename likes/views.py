from rest_framework import status
from rest_framework.viewsets import ModelViewSet, GenericViewSet, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import LikedItem
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .pagination import DefaultPagination
from .filters import LikedItemFilter
from .serializers import LikedItemSerializer, CreateLikedItemSerializer

# Create your views here.



class LikedItemViewSet(GenericViewSet,
            mixins.CreateModelMixin,
            mixins.DestroyModelMixin,
            mixins.ListModelMixin):
    
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = LikedItemFilter
    pagination_class = DefaultPagination
    search_fields = ['title', 'category']
    ordering_fields = ['title', 'category']

    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateLikedItemSerializer
        return LikedItemSerializer
    
    def get_queryset(self):
        return LikedItem.objects.filter(user=self.request.user, content_type__model="post")


