from django.db.models import Q
from rest_framework import filters
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets, status, permissions
from rest_framework.pagination import PageNumberPagination


from .models import Project, Task
from .pagination import get_pagination
from .permission import IsOwner, IsOwnerOrAssigned, IsOwnerOrMembers
from .serializer import ProjectListSerializer,ProjectCreateSeializer,\
                        ProjectDetailSerializer, ProjectUpdateSerializer, TaskListSerializer,\
                        TaskDetailSerializer, TaskCreateSerializer,TaskUpdateSerializer



class ProjectViewSet(viewsets.ViewSet):

    def get_permissions(self):
        """اعمال پرمیشن فقط برای متدهای خاص"""

        if self.action in ['project_update', 'project_delete','task_delete']:
            return [IsOwner()]
        if self.action in ['project_list', 'project_create','task_list', 'task_create']:
            return [permissions.IsAuthenticated()]
        if self.action in ['task_detail']:
            return [IsOwnerOrAssigned()]
        if self.action in ['project_detail']:
            return [IsOwnerOrMembers()]
        return [permissions.AllowAny()]
    
    
    def get_object(self, model,pk, select=None, perfech=None):
        """بررسی وجود پروژه و بازگردانی آن"""
        queryset = model.objects

        if select:
           queryset= queryset.select_related(*select)

        if perfech:
           queryset= queryset.prefetch_related(*perfech)

        return get_object_or_404(queryset, id=pk)
    

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

        paginator , project_paginator = get_pagination(queryset, request)
        

        serializer = ProjectListSerializer(project_paginator, many=True)
        return paginator.get_paginated_response(serializer.data)
    

    def project_detail(self, request, pk: int):
        """جزییات هر پروژه"""

        project = self.get_object(Project ,pk ,select=['owner'], perfech=['members'])
        self.check_object_permissions(request, project)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def project_create(self, request):
        """            ساخت پروژه توسط owner
          (فقط کاربران احراز شده می‌توانند پروژه ایجاد کنند)
        """

        serializer = ProjectCreateSeializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    def project_update(self, request, pk: int):
        """به‌روزرسانی پروژه فقط توسط مالک"""
        project = self.get_object(Project ,pk ,select=['owner'], perfech=['members'])


        self.check_object_permissions(request, project)

        serializer = ProjectUpdateSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def project_delete(self, request, pk: int):
        """حذف پروژه توسط صاحب پروژه"""
        project = self.get_object(Project ,pk ,select=['owner'], perfech=['members'])

        self.check_object_permissions(request, project)

        project.delete()
        return Response({'message': 'پروژه با موفقیت حذف شد.'}, status=status.HTTP_204_NO_CONTENT)
    

    def task_list(self, request):
        queryset = Task.objects.\
        select_related('project', 'assigned_user', 'owner').\
        filter(Q(owner=request.user) | Q(assigned_user=request.user)).\
        distinct()
        
        paginator , paginated_queryset = get_pagination(queryset, request)

        serializer = TaskListSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)
                   

    def task_detail(self, request, pk:int):
        queryset = self.get_object(Task, pk, select=['project','assigned_user'])
        self.check_object_permissions(request, queryset)
        serializer = TaskDetailSerializer(queryset)
        return Response(serializer.data)


    def task_create(self, request):
        serializer = TaskCreateSerializer(data= request.data, context={'request':request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'detail': 'با موفقیت ساخته شد'}, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    def task_update(self , request, pk):
        task = self.get_object(Task, pk, select=['project','assigned_user'])
        serializer = TaskUpdateSerializer(task ,data=request.data, partial=True, context={"request":request})
        
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'با موفقیت اپدیت شد'}, status=status.HTTP_200_OK)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    def task_delete(self, request, pk):
        task = self.get_object(Task, pk, select=['project','assigned_user'])
        self.check_object_permissions(request, task)
        
        task.delete()
        return Response({'message': 'تسک با موفقیت حذف شد.'}, status=status.HTTP_204_NO_CONTENT)
    


