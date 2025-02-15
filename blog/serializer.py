from rest_framework import serializers

from core.serializer import UserSerializer
from .models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id','content', 'post','user', 'created_at']
        read_only_fields= ['post', 'user']

    def create(self, validated_data):
        post_id = self.context['view'].kwargs['post_pk']
        post = Post.objects.get(id= post_id)
        user = self.context['request'].user

        validated_data['post']= post
        validated_data['user']= user

        return super().create(validated_data)
        

class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source ='author.full_name',read_only= True )
    category = serializers.CharField(source ='get_category_display')
    status = serializers.CharField(source ='get_status_display',read_only= True)
    like = serializers.SerializerMethodField(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)

    def get_like(self, post: Post):
        return post.likes.filter(user=self.context["request"].user).exists()
    
    def get_likes(self, post: Post):
        return post.likes.count()


    class Meta:
        model = Post
        fields = ['title','description','category','image','status','likes', 'like','views','author','created_at','update_at']

    def update(self, instance, validated_data):
        request = self.context.get('request')

        if request and request.method == "PATCH" and 'image' not in validated_data:
            validated_data['image'] = instance.image  

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class RetrievePostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source ='author.full_name',read_only= True )
    category = serializers.CharField(source ='get_category_display')
    status = serializers.CharField(source ='get_status_display',read_only= True)
    comments = CommentSerializer(many=True, read_only=True)
    like = serializers.SerializerMethodField(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)

    def get_like(self, post: Post):
        return post.likes.filter(user=self.context["request"].user).exists()
    
    def get_likes(self, post: Post):
        return post.likes.count()


    class Meta:
        model = Post
        fields = ['title','description','category','image','status','likes', 'like','views','author','update_at','comments']
        read_only_fields = ['views']



class CustomPostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only= True)
    category = serializers.CharField(source ='get_category_display')
    status = serializers.CharField(source ='get_status_display',read_only= True)
    like = serializers.SerializerMethodField(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)

    def get_like(self, post: Post):
        return post.likes.filter(user=self.context["request"].user).exists()
    
    def get_likes(self, post: Post):
        return post.likes.count()
    

    class Meta:
        model = Post
        fields = ['id','title','description','category', 'status','image','likes', 'like','views','author','created_at','update_at']
        read_only_fields = ['views']

 

class CreatePostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source ='author.full_name',read_only= True )
    class Meta:
        model = Post
        fields = ['title','description','category','image','status','author','created_at','update_at']
        read_only_fields = ['status']

    def create(self, validated_data):
        author = self.context['request'].user
        validated_data['author'] = author
        validated_data['status'] = 'UR'

        return super().create(validated_data)
    

class UpdatePostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source ='author.full_name',read_only= True )
    class Meta:
        model = Post
        fields = ['title','description','category','image','status','author', 'views','created_at','update_at']
        read_only_fields = ['views']

    def update(self, instance, validated_data):
        request = self.context.get('request')

        if request and request.method == "PATCH" and 'image' not in validated_data:
            validated_data['image'] = instance.image  
            
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
    



