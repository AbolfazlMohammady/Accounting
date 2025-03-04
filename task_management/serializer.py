from rest_framework import serializers
from django.contrib.auth import get_user_model
from core.serializer import UserSerializer
from django.utils import timezone
from datetime import timedelta

from .models import Task, Project


User = get_user_model()


class UserProject(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = [field for field in UserSerializer.Meta.fields if field not in {'phone', 'email', 'password'}] + ['full_name']
     

class _Project(serializers.ModelSerializer):
    owner = UserProject(read_only= True)
    members = UserProject(many=True)
    class Meta:
        model = Project
        fields= ['id','title','description','owner','members','created_at', 'update']


class ProjectListSerializer(_Project):
    pass

class UserFullNameRelatedField(serializers.PrimaryKeyRelatedField):
    def to_internal_value(self, data):
        try:
            user = User.objects.get(full_name=data)
        except User.DoesNotExist:
            raise serializers.ValidationError(f"User with full name '{data}' does not exist.")
        return user

    def to_representation(self, value):
        return value.full_name


class ProjectCreateSeializer(_Project):
    members = UserFullNameRelatedField(
        many=True, queryset=User.objects.all(), write_only=True
    )

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['owner'] = user   
        return super().create(validated_data)
    
    def validate(self, data):
        user = self.context['request'].user
        members = data.get('members',[])

        if user in members:
             raise serializers.ValidationError({"members": "مالک پروژه نباید جزو اعضای آن باشد."})

        return data
    
class ProjectDetailSerializer(_Project):
    class Meta(_Project.Meta):
        fields = [field for field in _Project.Meta.fields if field not in {'id'}]


class ProjectUpdateSerializer(_Project):
    members = UserFullNameRelatedField(
        many=True, queryset=Project.objects.all(),  write_only=True
    )
    class Meta(_Project.Meta):
        fields = ['title', 'description', 'members']

    def update(self, instance, validated_data):
        members_data = validated_data.pop('members',None)

        for attr, value in validated_data.items():
            setattr(instance, attr,value)

        if members_data is not None:
            instance.members.set(members_data)
        
        instance.save()
        return instance

    # def update(self, instance, validated_data):
    #     allowed_fields = {'title', 'description', 'members'}
        
    #     filtered_data = {key: value for key, value in validated_data.items() if key in allowed_fields}

    #     return super().update(instance, filtered_data)


class TaskProjectSerializer(_Project):
    class Meta(_Project.Meta):
        fields = [field for field in _Project.Meta.fields if field not in {'id','description','owner','members','created_at', 'update'}]


class _Task(serializers.ModelSerializer):
    project = TaskProjectSerializer()
    assigned_user = UserProject(required=False)
    owner = UserProject(read_only=True)
    status = serializers.CharField(source ='get_status_display',read_only= True)

    class Meta:
        model= Task
        fields= [
            'id', 
            'title', 
            'description', 
            'project', 
            'owner',
            'assigned_user',
            'score', 
            'status', 
            'start_time', 
            'due_time', 
            'completed_at', 
            'completed'
        ]


class TaskListSerializer(_Task):
    start_time = serializers.SerializerMethodField()
    completed_at = serializers.SerializerMethodField()
    due_time = serializers.SerializerMethodField()

    def get_start_time(self, obj: Task):
        if not obj.start_time:
            return "نامشخص"

        now = timezone.now()
        delta = now - obj.start_time

        if delta < timedelta(hours=24):
            return f"{delta.seconds // 3600} ساعت پیش"
        else:
            return f"{delta.days} روز پیش"
        
    def get_completed_at(self, obj:Task):
        if not obj.completed_at:
            return 'تکمیل نشده'
        
        now = timezone.now()
        delta = now - obj.completed_at

        if delta < timedelta(hours=24):
            return f"{delta.seconds // 3600} ساعت پیش"
        else:
            return f"{delta.days} روز پیش"
        
    def get_due_time(self, obj:Task):
        if not obj.due_time:
            return 'مشخص نشده هنوز'
        
        now = timezone.now()
        delta = now - obj.due_time

        if delta < timedelta(hours=24):
            return f"{delta.seconds // 3600} ساعت "
        else:
            return f"{delta.days} روز "


class TaskDetailSerializer(_Task):
    start_time = serializers.SerializerMethodField()
    completed_at = serializers.SerializerMethodField()
    due_time = serializers.SerializerMethodField()

    class Meta(_Task.Meta):
        fields= [field for field in _Task.Meta.fields if field not in {'id'}]
    

    def get_start_time(self, obj: Task):
        if not obj.start_time:
            return "نامشخص"

        now = timezone.now()
        delta = now - obj.start_time

        if delta < timedelta(hours=24):
            return f"{delta.seconds // 3600} ساعت پیش"
        else:
            return f"{delta.days} روز پیش"
        
    def get_completed_at(self, obj:Task):
        if not obj.completed_at:
            return 'تکمیل نشده'
        
        now = timezone.now()
        delta = now - obj.completed_at

        if delta < timedelta(hours=24):
            return f"{delta.seconds // 3600} ساعت پیش"
        else:
            return f"{delta.days} روز پیش"
        
    def get_due_time(self, obj:Task):
        if not obj.due_time:
            return 'مشخص نشده هنوز'
        
        now = timezone.now()
        delta = now - obj.due_time

        if delta < timedelta(hours=24):
            return f"{delta.seconds // 3600} ساعت "
        else:
            return f"{delta.days} روز "


class TitleTaskPrimekeySerializer(serializers.PrimaryKeyRelatedField):
    def to_internal_value(self, data):
        try:
            project = Project.objects.get(title=data)
        except:
            raise serializers.ValidationError(f'canot find project <<{data}>>')
        return project
    
    def to_representation(self, value):
        return value.title


class TaskCreateSerializer(_Task):
    assigned_user= UserFullNameRelatedField(queryset=User.objects.all(), required=False)
    project = TitleTaskPrimekeySerializer(queryset=Project.objects.all(),  write_only=True ,required=False)

    class Meta(_Task.Meta):
        fields= [field for field in _Task.Meta.fields if field not in {'id'}]
        read_only_fields = ['start_time','completed_at']
    
    def create(self, validated_data):
        user = self.context['request'].user
        assigned_user = validated_data.get('assigned_user', None)

        
        project_data = validated_data.pop('project', None)
        if not project_data:
            raise serializers.ValidationError({'error': "پروژه باید مشخص باشد."})

        try:
            project = Project.objects.get(title=project_data)  
        except Project.DoesNotExist:
            raise serializers.ValidationError({'error': "پروژه‌ای با این نام یافت نشد."})

        if user != project.owner:
            raise serializers.ValidationError({'error': 'مالک تسک باید با مالک پروژه یکی باشد'})

        validated_data['owner'] = user
        
        if assigned_user:
            validated_data['start_time'] = timezone.now()
            validated_data['status'] = 'IP'
        else:
            validated_data['status'] = 'P'


        task = Task.objects.create(project=project, **validated_data)
        return task


class TaskUpdateSerializer(_Task):
    assigned_user= UserFullNameRelatedField(queryset=User.objects.all(), required=False)

    def update(self, instance, validated_data):
        user = self.context['request'].user
        assigned_user = validated_data.get('assigned_user', instance.assigned_user)
        completed = validated_data.get('completed', instance.completed)

        if 'assigned_user' in validated_data and user != instance.owner:
            raise serializers.ValidationError({'assigned_user': 'فقط مالک پروژه می‌تواند کاربر مسئول تسک را تغییر دهد.'})

        if 'assigned_user' in validated_data and assigned_user not in instance.project.members.all():
            raise serializers.ValidationError({'assigned_user': 'کاربری که اضافه میکنید باید تو لیست پروژه باشد'})


        if 'completed' in validated_data and user != instance.assigned_user:
            raise serializers.ValidationError({'completed': 'فقط کسی که تسک به او اختصاص داده شده می‌تواند وضعیت آن را تغییر دهد.'})

        if assigned_user and not instance.start_time:
            validated_data['start_time'] = timezone.now()
            validated_data['status'] = 'IP'

        if completed:
            validated_data['completed_at'] = timezone.now()

            start_time = instance.start_time or validated_data.get('start_time')
            completed_at = validated_data['completed_at']

            if start_time and completed_at and instance.due_time:
                duration = completed_at - start_time
                deadline_duration = instance.due_time - start_time

                if duration <= deadline_duration:
                    early_completion_seconds = (deadline_duration - duration).total_seconds()
                    early_completion_hours = int(early_completion_seconds // 3600) 

                    print(early_completion_seconds)
                    print(early_completion_hours)
                    print("=" * 30)

                    score = min(10, early_completion_hours)  
                    print(score)
                    validated_data['score'] = score
                    validated_data['status'] = 'C'
                    print(f"✅ مقدار دهی شده به validated_data: {validated_data['score']}")
                else:
                    delay_seconds = (completed_at - instance.due_time).total_seconds()
                    delay_hours = int(delay_seconds // 3600)  
                    score = max(-10, -delay_hours)  
                    validated_data['score'] = score
                    validated_data['status'] = 'F'
            else:
                validated_data['score'] = 0

        instance = super().update(instance, validated_data)
        instance.save()
        instance.refresh_from_db()

        return instance






