from django.db.models import Q
from rest_framework import filters
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


from .models import Project, Task
from .serializer import ProjectListSerializer,ProjectCreateSeializer,\
                        ProjectDetailSerializer, ProjectUpdateSerializer



class ProjectViewSet(viewsets.ViewSet):

    def get_object(self, pk):
        """بررسی وجود پروژه و بازگردانی آن"""
        try:
            return Project.objects.get(id=pk)
        except Project.DoesNotExist:
            return None

    def project_list(self, request):
        """ لیست پروژه‌هایی که کاربر عضو یا مالک آن‌هاست."""
        user = request.user

        if request.user.is_authenticated:  
            queryset = Project.objects\
                .select_related('owner')\
                .prefetch_related('members')\
                .filter(Q(members=user) | Q(owner=user))\
                .only('id', 'title', 'description', 'owner', 'created_at', 'update')\
                .distinct().order_by('-update')  
        else:  
            # می‌توانید در اینجا مشخص کنید که در صورت لاگین نبودن کاربر، چه چیزی را برگردانید  
            queryset = Project.objects.none()

        search_query = request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        created_after = request.query_params.get('created_after', None)
        if created_after:
            queryset = queryset.filter(created_at__gte=created_after)


        paginator = PageNumberPagination()
        paginator.page_size = 6
        project_paginator = paginator.paginate_queryset(queryset, request)

        serializer = ProjectListSerializer(project_paginator, many=True)
        return paginator.get_paginated_response(serializer.data)


    def project_detail(self, request, pk:int):
        """جزییات هر پروژه"""
        project = self.get_object(pk)
        if not project:
            return Response({'error': "پروژه پیدا نشد!"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer=  ProjectDetailSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def project_create(self, request):
        """ساخت پروژه توسط  owner (فقط کاربران احراز شده می‌توانند پروژه ایجاد کنند)"""
        if not request.user or request.user.is_anonymous:
            return Response({"detail": "شما احراز هویت نشده‌اید."}, status=status.HTTP_401_UNAUTHORIZED)
    
        
        serializer = ProjectCreateSeializer(data=request.data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

    def project_update(self, request, pk: int):
        """به‌روزرسانی پروژه فقط توسط مالک"""
        project = self.get_object(pk)
        if not project:
            return Response({'error': "پروژه پیدا نشد!"}, status=status.HTTP_404_NOT_FOUND)

        if project.owner_id != request.user.id:
            return Response({'error': 'فقط صاحب پروژه می‌تواند تغییرات اعمال کند.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = ProjectUpdateSerializer(project, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def project_delete(self, request, pk:int):
        """حذف پروژه توسط صاحب پروژه"""
        project = self.get_object(pk)
        if not project:
            return Response({'error': "پروژه پیدا نشد!"}, status=status.HTTP_404_NOT_FOUND)
        
        if project.owner_id != request.user.id:
            return Response({'error': 'فقط صاحب پروژه می‌تواند تغییرات اعمال کند.'}, status=status.HTTP_403_FORBIDDEN)

        project.delete()
        return Response({'message': 'پروژه با موفقیت حذف شد.'}, status=status.HTTP_204_NO_CONTENT)


