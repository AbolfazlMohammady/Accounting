from django.urls import path, include
# from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()
router.register('', views.PostViewSet, basename='posts')

blog_router = routers.NestedDefaultRouter(router, '', lookup='post')
blog_router.register('comment', views.CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(blog_router.urls)),
]
