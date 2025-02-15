from rest_framework import serializers
from django.apps import apps
from .models import LikedItem



class LikedItemSerializer(serializers.ModelSerializer):
    content_type = serializers.SerializerMethodField()
    object = serializers.SerializerMethodField()
    
    def get_object(self, liked_item: LikedItem):
        # همان کد قبلی برای دریافت آبجکت لایک شده
        object_id = liked_item.object_id
        content_type = liked_item.content_type
        model_content = apps.get_model(content_type.app_label, content_type.model)
        
        try:
            object_liked = model_content.objects.get(id=object_id)
            id = object_liked.id
            image = object_liked.image
            title = object_liked.title  # فرض کنید این فیلد برای پست موجود است
            return {"id": id, "title": title, "image": image.url if image else None}
        except:
            return "همچین آبجکتی وجود ندارد"
    
    def get_content_type(self, liked_item: LikedItem):
        # اگر فقط می‌خواهید مدل ثابت "post" نمایش داده شود:
        return {"model": "post"}
    
    class Meta:
        model = LikedItem
        fields = ['id', 'user', 'object_id', 'object', 'content_type']
        read_only_fields = ['user']



class CreateLikedItemSerializer(serializers.ModelSerializer):
    def validate_content_type(self, content_type):
        allowed_models = ['post']  # فقط مدل‌های مجاز
        if content_type.model not in allowed_models:
            raise serializers.ValidationError("فقط می‌توان پست‌های بلاگ را لایک کرد!")
        return content_type
    
    def validate(self, liked_item):
        object_id = liked_item["object_id"]
        content_type = liked_item["content_type"]
        
        # بررسی اینکه آبجکت مورد نظر در مدل post وجود داشته باشد
        if content_type.model == "post":
            model_content = apps.get_model(content_type.app_label, content_type.model)
            if not model_content.objects.filter(id=object_id).exists():
                raise serializers.ValidationError({"object_id": "این پست بلاگ وجود ندارد!"})
        else:
            raise serializers.ValidationError("مدل انتخاب شده معتبر نیست!")

        return liked_item
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    class Meta:
        model = LikedItem
        fields = ['id', 'user', 'object_id', 'content_type']
        read_only_fields = ['user']
