from rest_framework import serializers
from django.contrib.auth import get_user_model
from core.serializer import UserSerializer

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

