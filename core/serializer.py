from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model= User
        fields = ['phone', 'email','password']
        extra_kwargs = {"password": {"write_only": True}}

        
class ProfileSeializer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields = ['phone', 'email','full_name', 'image', 'age', 'role', 'gender', 'bio']

