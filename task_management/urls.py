from django.urls import path, include

from .views import ProjectViewSet


urlpatterns = [
    path('', ProjectViewSet.as_view({
        'get': 'project_list'
    })),
    path('<int:pk>/', ProjectViewSet.as_view({
        'get': 'project_detail',
        'patch': 'project_update',
        'delete': 'project_delete',
    })),
    path('create/', ProjectViewSet.as_view({
        'post': 'project_create'
    })),
    path('task/', ProjectViewSet.as_view({
        'get': 'task_list',
    })),
        path('task/<int:pk>/', ProjectViewSet.as_view({
        'get': 'task_detail',
        'patch': 'task_update',
        'delete': 'task_delete',
    })),
    path('task/create/', ProjectViewSet.as_view({
        'post': 'task_create'
    })),
]