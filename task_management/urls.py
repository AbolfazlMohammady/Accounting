from django.urls import path, include

from .views import ProjectViewSet


urlpatterns = [
    path('', ProjectViewSet.as_view({
        'get': 'project_list'
    })),
    path('<int:pk>/', ProjectViewSet.as_view({
        'get': 'project_detail',
        'patch': 'project_update'
    })),
    path('create/', ProjectViewSet.as_view({
        'post': 'project_create'
    }))
]