from django.db.models import Q
from rest_framework import filters
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets, status, permissions
from rest_framework.pagination import PageNumberPagination


from .permission import IsOwner
from .models import Project, Task
from .serializer import ProjectListSerializer,ProjectCreateSeializer,\
                        ProjectDetailSerializer, ProjectUpdateSerializer



class ProjectViewSet(viewsets.ViewSet):

    def get_permissions(self):
        """اعمال پرمیشن فقط برای متدهای خاص"""

        if self.action in ['project_update', 'project_delete']:
            return [IsOwner()]
        if self.action in ['project_list', 'project_create']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
    
    def get_object(self, pk):
        """بررسی وجود پروژه و بازگردانی آن"""
        return get_object_or_404(Project, id=pk)

    def filter_projects(self, queryset, request):
        """اعمال فیلترها برای لیست پروژه‌ها"""

        search_query = request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        created_after = request.query_params.get('created_after', None)
        if created_after:
            queryset = queryset.filter(created_at__gte=created_after)
        
        return queryset

    def project_list(self, request):
        """لیست پروژه‌هایی که کاربر عضو یا مالک آن‌هاست."""
        user = request.user 
        queryset = Project.objects\
            .select_related('owner')\
            .prefetch_related('members')\
            .filter(Q(members=user) | Q(owner=user))\
            .only('id', 'title', 'description', 'owner', 'created_at', 'update')\
            .distinct().order_by('-created_at')  

        queryset = self.filter_projects(queryset, request)

        paginator = PageNumberPagination()
        paginator.page_size = 6
        project_paginator = paginator.paginate_queryset(queryset, request)

        serializer = ProjectListSerializer(project_paginator, many=True)
        return paginator.get_paginated_response(serializer.data)
    

    def project_detail(self, request, pk: int):
        """جزییات هر پروژه"""
        project = self.get_object(pk)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def project_create(self, request):
        """ساخت پروژه توسط owner (فقط کاربران احراز شده می‌توانند پروژه ایجاد کنند)"""

        serializer = ProjectCreateSeializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    def project_update(self, request, pk: int):
        """به‌روزرسانی پروژه فقط توسط مالک"""
        project = self.get_object(pk)

        self.check_object_permissions(request, project)

        serializer = ProjectUpdateSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def project_delete(self, request, pk: int):
        """حذف پروژه توسط صاحب پروژه"""
        project = self.get_object(pk)
        self.check_object_permissions(request, project)

        project.delete()
        return Response({'message': 'پروژه با موفقیت حذف شد.'}, status=status.HTTP_204_NO_CONTENT)

